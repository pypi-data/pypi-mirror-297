import time

import os
import random
import subprocess
import torch
from params_proto import ParamsProto, Proto
from params_proto.hyper import Sweep
from pathlib import Path
from zaku import TaskQ

from lucidsim.traj_samplers.unroll_flow_stream import Unroll_flow_stream as Unroll_s


class LucidSimDaggerRunner(ParamsProto, prefix="dagger"):
    collection_name: str = "extensions_hurdle_cone_cobblestone_prompts_v1"

    env_name = "Extensions-cones-hurdle_one-lucidsim-v1"
    dagger_env_name = "Extensions-cones-hurdle_one-lucidsim_sampling-v1"

    control_strength = 0.7
    cone_strength = 1.5
    workflow_cls = "weaver.workflows.three_mask_workflow:ImagenCone"

    runner_prefix = "/lucidsim/lucidsim/corl/lucidsim_datasets/debug/extensions_hurdle_cone_cobblestone_prompts_v1-flow_7"

    teacher_queue_name = Proto(env="$ZAKU_USER:lucidsim:flow-teacher-queue-1")
    training_queue_name = Proto(env="$ZAKU_USER:lucidsim:trainer-queue-1")

    num_dagger_iters = 3
    baseline_interval = 7
    model_stack_size = 7

    traj_count = 500

    seed = 42
    teacher_checkpoint = "/lucid-sim/lucid-sim/baselines/launch_gains/2024-03-20/04.03.35/go1/300/20/0.5/checkpoints/model_last.pt"
    initial_checkpoints_prefix = "/lucid-sim/lucid-sim/baselines/launch_intermediate_ckpts_v3/go1/delay_4"

    local_data_root = Proto(env="$DATASETS/lucidsim")
    rsync_source_prefix = "luma01:datasets/lucidsim/"

    flow_camera_name = "ego-rgb-render"

    rollout_seed_offset = 0
    offline_generation = False

    debug = False


def create_initial_sweep(dagger_iter, prev_checkpoint=None):
    from ml_logger import logger

    random.seed(LucidSimDaggerRunner.seed)

    collections_root = Path(__file__).parent / "datasets" / "lucidsim_v1" / "_collections"

    if isinstance(LucidSimDaggerRunner.collection_name, str):
        prompt_list = Sweep.read(f"{collections_root}/{LucidSimDaggerRunner.collection_name}.jsonl")
    else:
        prompt_list = []
        for collection_name in LucidSimDaggerRunner.collection_name:
            prompt_list += Sweep.read(f"{collections_root}/{collection_name}.jsonl")

    if dagger_iter == 0:
        with logger.Prefix(LucidSimDaggerRunner.initial_checkpoints_prefix):
            checkpoint_paths = logger.glob("**/checkpoints/*.pt")

        checkpoint_paths = [f"{LucidSimDaggerRunner.initial_checkpoints_prefix}/{path}" for path in checkpoint_paths] * int(
            LucidSimDaggerRunner.traj_count / len(checkpoint_paths)
        ) + [LucidSimDaggerRunner.teacher_checkpoint] * LucidSimDaggerRunner.traj_count

        random.shuffle(checkpoint_paths)

        checkpoint_paths = checkpoint_paths[: LucidSimDaggerRunner.traj_count]
    else:
        # from previous iter
        checkpoint_paths = [prev_checkpoint] * LucidSimDaggerRunner.traj_count

    dataset_path = f"{LucidSimDaggerRunner.runner_prefix}/datasets/dagger_{dagger_iter}"

    with Sweep(Unroll_s) as sweep:
        Unroll_s.render = True
        Unroll_s.stop_after_termination = True

        Unroll_s.vision_key = "imagen" if dagger_iter > 0 else None
        Unroll_s.env_name = LucidSimDaggerRunner.env_name if dagger_iter == 0 else LucidSimDaggerRunner.dagger_env_name
        Unroll_s.model_entrypoint = (
            "behavior_cloning.go1_model.transformers.transformer_policy:get_rgb_transformer_policy_batchnorm"
            if dagger_iter > 0
            else "cxx.modules.parkour_actor:get_parkour_teacher_policy"
        )

        Unroll_s.logger_prefix = dataset_path
        Unroll_s.baseline_interval = LucidSimDaggerRunner.baseline_interval
        Unroll_s.width = 320
        Unroll_s.height = 180

        with sweep.product:
            Unroll_s.checkpoint = checkpoint_paths

    jobs = []
    for rollout_id, dep in enumerate(sweep):
        dep["unroll.seed"] = rollout_id + LucidSimDaggerRunner.rollout_seed_offset
        dep["unroll.flow_camera_name"] = LucidSimDaggerRunner.flow_camera_name
        dep["unroll.offline_generation"] = LucidSimDaggerRunner.offline_generation
        dep["control_strength"] = LucidSimDaggerRunner.control_strength
        dep["cone_strength"] = LucidSimDaggerRunner.cone_strength
        dep["rollout_id"] = f"{rollout_id + LucidSimDaggerRunner.rollout_seed_offset:04d}"
        dep["rollout_id"] = f"{rollout_id:04d}"
        dep["prompt_list"] = random.sample(prompt_list, len(prompt_list))
        dep["render_kwargs"] = {
            "workflow_cls": LucidSimDaggerRunner.workflow_cls,
            "downscale": 4,
            "crop_size": (1280, 720),
        }

        jobs.append(dep)

    return jobs[: 2 if LucidSimDaggerRunner.debug else None], dataset_path


def main(_deps=None, dagger_start=None, **deps):
    from ml_logger import logger
    from lucidsim_experiments import RUN

    try:  # RUN.prefix is a template, will raise error.
        RUN._update(_deps)
        logger.configure(RUN.prefix)
    except KeyError:
        pass

    LucidSimDaggerRunner._update(_deps, **deps)

    flow_teacher_queue = TaskQ(name=LucidSimDaggerRunner.teacher_queue_name)
    print("Flow teacher queue:", flow_teacher_queue.name)
    training_queue = TaskQ(name=LucidSimDaggerRunner.training_queue_name)
    print("Training queue:", training_queue.name)

    logger.job_started(dagger=vars(LucidSimDaggerRunner))
    print(logger.get_dash_url())

    dagger_datasets = []

    current_student_checkpoint = None

    if dagger_start is None:
        dagger_start = 0

    assert dagger_start <= LucidSimDaggerRunner.num_dagger_iters, "dagger_start should be less than or equal to num_dagger_iters."

    for dagger_iter in range(LucidSimDaggerRunner.num_dagger_iters + 1):
        data_sweep, dataset_path = create_initial_sweep(dagger_iter, prev_checkpoint=current_student_checkpoint)
        dagger_datasets.append(dataset_path.lstrip("/"))
        logger.save_json(data_sweep, f"dagger_{dagger_iter}.jsonl")

        # upload, wait for job to finish
        starting_len = len(data_sweep)
        logger.print("Adding", starting_len, "jobs to the flow teacher queue.")

        stale_threshold = 0.1
        stale_timeout = 60 * 30  # 30 min
        stale_start_time = None
        stale_count = float("inf")

        if dagger_iter >= dagger_start:
            is_done, tokens = flow_teacher_queue.gather(data_sweep, gather_tokens=None)
            assert len(tokens) == starting_len, "Tokens should be the same length as the number of jobs."
            while not is_done(blocking=False):
                print(f"{len(tokens)} jobs left.")
                time.sleep(2.0)

                if len(tokens) < starting_len * stale_threshold:
                    if stale_start_time is None:
                        stale_start_time = time.time()
                        continue
                    if time.time() - stale_start_time > stale_timeout:
                        if len(tokens) >= stale_count:
                            logger.print("Stale timeout reached. Exiting early.")
                            break
                        else:
                            stale_count = min(len(tokens), stale_count)

                flow_teacher_queue.unstale_tasks(10)

            logger.print("Flow teacher done, waiting a bit for images to save...")
            time.sleep(20.0)
        else:
            logger.print("Skipping flow teacher queue for dagger_iter", dagger_iter)

        # Pull images to local filesystem
        local_destination = Path(LucidSimDaggerRunner.local_data_root) / Path(dataset_path).relative_to("/")
        local_destination.mkdir(parents=True, exist_ok=True)

        dataset_sync_command = [
            "rsync",
            "-avzhr",
            os.path.join(LucidSimDaggerRunner.rsync_source_prefix, str(Path(dataset_path).relative_to("/"))),
            f"{local_destination.parent}/",
            "--info=progress2",
        ]

        try:
            result = subprocess.run(dataset_sync_command, check=True, text=True, capture_output=True)
            logger.print("Dataset sync completed successfully.")
            logger.print("Output:", result.stdout)
        except subprocess.CalledProcessError as e:
            logger.print("Dataset sync failed with error:", e.stderr)

        # train and feed into the next
        train_root = f"/{logger.prefix}/train/dagger_{dagger_iter}"

        training_job = {
            "train.dataset_prefix": dagger_datasets,
            "train.logical_img_dim": 3,
            "train.stack_size": LucidSimDaggerRunner.model_stack_size,
            "train.image_type": f"augmented_{LucidSimDaggerRunner.baseline_interval}",
            "train.use_batchnorm": True,
            "train.teacher_checkpoint": LucidSimDaggerRunner.teacher_checkpoint,
            "train.student_checkpoint": current_student_checkpoint,
            "train.n_epochs": 70,
            "train.delay": 0,
            "train.debug": LucidSimDaggerRunner.debug,
            "RUN.prefix": train_root,
        }

        tokens = None

        if dagger_iter >= dagger_start:
            is_done, tokens = training_queue.gather_one(training_job, tokens)

            print("Training started.")
            while not is_done(blocking=False):
                print("Training...", len(tokens))
                training_queue.unstale_tasks(10)
                time.sleep(2.0)
        else:
            logger.print("Skipping training for dagger_iter", dagger_iter)

        next_checkpoint = validate_checkpoint(train_root)
        if next_checkpoint is None:
            logger.print("No clean checkpoint found. Something went wrong, please review. Stopping this run.")
            break

        current_student_checkpoint = f"{train_root}/{next_checkpoint}"
        logger.print("Training done! Proceeding to next dagger iteration after sleeping a bit.")
        time.sleep(10.0)


def validate_checkpoint(train_root):
    from ml_logger import logger

    with logger.Prefix(train_root):
        checkpoints = sorted(logger.glob("checkpoints/*.pt"), reverse=True)

        clean_ckpt = None
        for checkpoint in checkpoints:
            sd = logger.torch_load(checkpoint)
            # check if any weight is nan
            for k, v in sd.items():
                if torch.isnan(v).any():
                    logger.print(f"Found nan in {k}!")
                    break
            else:
                logger.print(f"Checkpoint {checkpoint} is clean.")
                clean_ckpt = checkpoint
                break

    return clean_ckpt


if __name__ == "__main__":
    exit()
    # q_name = "alanyu:lucidsim:trainer-queue-1"
    # q = TaskQ(name=q_name)
    # q.clear_queue()
    #
    q = TaskQ(name="alanyu:lucidsim:flow-teacher-queue-1")
    q.clear_queue()
    #

    q = TaskQ(name="alanyu:lucidsim:trainer-queue-1")
    q.clear_queue()
    exit()
    #
    # # sleep(2.0)
    # deps = {
    #     "dagger.collection_name": "extensions_cones_stairs_bcs_prompts_v7",
    #     "dagger.env_name": "Extensions-cones-stairs_wh-lucidsim-v1",
    #     "dagger.dagger_env_name": "Extensions-cones-stairs_wh-lucidsim_sampling-v1",
    #     "dagger.traj_count": 1000,
    #     "dagger.runner_prefix": "/lucidsim/lucidsim/corl/lucidsim_datasets/extensions_cones_stairs_wh-bcs_prompts_v7_v2",
    #     "dagger.teacher_checkpoint": "/instant-feature/scratch/2024/05-18/220933/checkpoints/model_last.pt",
    #     "dagger.initial_checkpoints_prefix": "/instant-feature/scratch/2024/05-18/220933",
    #     "dagger.control_strength": 1.0,
    #     "dagger.teacher_queue_name": "alanyu:lucidsim:debug-flow-teacher-queue-1",
    #     "RUN.job_counter": 1,
    #     "RUN.prefix": "lucidsim/lucidsim/corl_experiments/datasets/lucidsim_v1/extensions_cones_stairs_wh-bcs_prompts_v7_v1/sweep_v2/sweep/Extensions-cones-stairs_wh-lucidsim-v1",
    #     "RUN.job_name": "Extensions-cones-stairs_wh-lucidsim-v1",
    # }
    #
    # if dagger_iter >= dagger_start:
    #     is_done, tokens = training_queue.gather_one(training_job, tokens)
    #
    #     print("Training started.")
    #     while not is_done(blocking=False):
    #         print("Training...")
    #         training_queue.unstale_tasks(10)
    #         time.sleep(2.0)
    # else:
    #     logger.print("Skipping training for dagger_iter", dagger_iter)
