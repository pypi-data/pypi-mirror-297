import os
import random
import subprocess
import torch
from params_proto import ParamsProto, Proto
from params_proto.hyper import Sweep
from pathlib import Path
from zaku import TaskQ

from lucidsim.traj_samplers.unroll_stream import Unroll_stream as Unroll_s


class DepthDaggerRunner(ParamsProto, prefix="dagger"):
    env_name = "Extensions-cones-hurdle_one-render_depth-v1"
    dagger_env_name = "Extensions-cones-hurdle_one-vision_depth_dagger-v1"

    runner_prefix = "/lucidsim/lucidsim/corl/baseline_datasets/debug/depth/extensions_cones_hurdle_one"

    teacher_queue_name = Proto(env="$ZAKU_USER:lucidsim:depth-teacher-queue-1")
    training_queue_name = Proto(env="$ZAKU_USER:lucidsim:depth-trainer-queue-1")

    num_dagger_iters = 3

    stack_size = 7

    traj_count = 1_000

    seed = 42
    teacher_checkpoint = "/lucid-sim/lucid-sim/baselines/launch_gains/2024-03-20/04.03.35/go1/300/20/0.5/checkpoints/model_last.pt"
    initial_checkpoints_prefix = "/lucid-sim/lucid-sim/baselines/launch_intermediate_ckpts_v3/go1/delay_4"

    local_data_root = Proto(env="$DATASETS/lucidsim")
    rsync_source_prefix = "luma01:datasets/lucidsim/"

    debug = False


def create_initial_sweep(dagger_iter, prev_checkpoint=None):
    from ml_logger import logger

    random.seed(DepthDaggerRunner.seed)

    if dagger_iter == 0:
        with logger.Prefix(DepthDaggerRunner.initial_checkpoints_prefix):
            checkpoint_paths = logger.glob("**/checkpoints/*.pt")

        checkpoint_paths = [f"{DepthDaggerRunner.initial_checkpoints_prefix}/{path}" for path in checkpoint_paths] * int(
            DepthDaggerRunner.traj_count / len(checkpoint_paths)
        ) + [DepthDaggerRunner.teacher_checkpoint] * DepthDaggerRunner.traj_count

        random.shuffle(checkpoint_paths)

        checkpoint_paths = checkpoint_paths[: DepthDaggerRunner.traj_count]
    else:
        # from previous iter
        checkpoint_paths = [prev_checkpoint] * DepthDaggerRunner.traj_count

    dataset_path = f"{DepthDaggerRunner.runner_prefix}/datasets/dagger_{dagger_iter}"

    with Sweep(Unroll_s) as sweep:
        Unroll_s.render = True
        Unroll_s.stop_after_termination = True

        Unroll_s.vision_key = "vision" if dagger_iter > 0 else None
        Unroll_s.env_name = DepthDaggerRunner.env_name if dagger_iter == 0 else DepthDaggerRunner.dagger_env_name
        Unroll_s.model_entrypoint = (
            "behavior_cloning.go1_model.transformers.transformer_policy:get_depth_transformer_policy"
            if dagger_iter > 0
            else "cxx.modules.parkour_actor:get_parkour_teacher_policy"
        )

        Unroll_s.logger_prefix = dataset_path
        Unroll_s.width = 320
        Unroll_s.height = 180

        with sweep.product:
            Unroll_s.checkpoint = checkpoint_paths

    jobs = []
    for rollout_id, dep in enumerate(sweep):
        dep["unroll.seed"] = rollout_id
        dep["rollout_id"] = f"{rollout_id:04d}"

        jobs.append(dep)

    return jobs[: 1 if DepthDaggerRunner.debug else None], dataset_path


def main(_deps=None, **deps):
    from ml_logger import logger
    from lucidsim_experiments import RUN
    import time

    try:  # RUN.prefix is a template, will raise error.
        RUN._update(_deps)
        logger.configure(RUN.prefix)
    except KeyError:
        pass

    depth_teacher_queue = TaskQ(name=DepthDaggerRunner.teacher_queue_name)
    training_queue = TaskQ(name=DepthDaggerRunner.training_queue_name)

    DepthDaggerRunner._update(_deps, **deps)

    logger.job_started(dagger=vars(DepthDaggerRunner))
    print(logger.get_dash_url())

    dagger_datasets = []

    current_student_checkpoint = None

    for dagger_iter in range(DepthDaggerRunner.num_dagger_iters + 1):
        data_sweep, dataset_path = create_initial_sweep(dagger_iter, prev_checkpoint=current_student_checkpoint)
        dagger_datasets.append(dataset_path.lstrip("/"))
        logger.save_json(data_sweep, f"dagger_{dagger_iter}.jsonl")

        # upload, wait for job to finish
        starting_len = len(data_sweep)
        print("Adding", starting_len, "jobs to the depth teacher queue.")

        stale_threshold = 0.1
        stale_timeout = 60 * 30  # 30 min
        stale_start_time = None

        is_done, tokens = depth_teacher_queue.gather(data_sweep, gather_tokens=None)
        assert len(tokens) == starting_len, "Tokens should be the same length as the number of jobs."
        while not is_done(blocking=False):
            print(f"{len(tokens)} jobs left.")
            time.sleep(2.0)

            if len(tokens) < starting_len * stale_threshold and stale_start_time is None:
                stale_start_time = time.time()
            elif len(tokens) < starting_len * stale_threshold and time.time() - stale_start_time > stale_timeout:
                logger.print("Good enough. Exiting early.")
                break

            depth_teacher_queue.unstale_tasks(10)

        logger.print("Flow teacher done, waiting a bit for images to save...")
        time.sleep(20.0)

        # Pull images to local filesystem

        local_destination = Path(DepthDaggerRunner.local_data_root) / Path(dataset_path).relative_to("/")
        local_destination.mkdir(parents=True, exist_ok=True)

        dataset_sync_command = [
            "rsync",
            "-avzhr",
            os.path.join(DepthDaggerRunner.rsync_source_prefix, str(Path(dataset_path).relative_to("/"))),
            f"{local_destination.parent}/",
            "--info=progress2",
        ]

        try:
            result = subprocess.run(dataset_sync_command, check=True, text=True, capture_output=True)
            print("Dataset sync completed successfully.")
            print("Output:", result.stdout)
        except subprocess.CalledProcessError as e:
            print("Dataset sync failed with error:", e.stderr)

        # train and feed into the next
        train_root = f"/{logger.prefix}/train/dagger_{dagger_iter}"

        training_job = {
            "train.dataset_prefix": dagger_datasets,
            "train.logical_img_dim": 1,
            "train.image_type": "depth",
            "train.stack_size": DepthDaggerRunner.stack_size,
            "train.use_batchnorm": False,
            "train.teacher_checkpoint": DepthDaggerRunner.teacher_checkpoint,
            "train.student_checkpoint": current_student_checkpoint,
            "train.n_epochs": 70,
            "train.debug": DepthDaggerRunner.debug,
            "RUN.prefix": train_root,
        }

        tokens = None
        is_done, tokens = training_queue.gather_one(training_job, tokens)

        print("Training started.")
        while not is_done(blocking=False):
            print("Training...")
            training_queue.unstale_tasks(10)
            time.sleep(2.0)

        next_checkpoint = validate_checkpoint(train_root)
        if next_checkpoint is None:
            print("No clean checkpoint found. Something went wrong, please review. Stopping this run.")
            break

        current_student_checkpoint = f"{train_root}/{next_checkpoint}"
        print("Training done! Proceeding to next dagger iteration after sleeping a bit.")
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
                    print(f"Found nan in {k}!")
                    break
            else:
                print(f"Checkpoint {checkpoint} is clean.")
                clean_ckpt = checkpoint
                break

    return clean_ckpt


if __name__ == "__main__":
    # q = TaskQ(name="alanyu:lucidsim:depth-teacher-queue-1")
    # q.clear_queue()

    q = TaskQ(name="alanyu:lucidsim:trainer-queue-1")
    q.clear_queue()

    # main(debug=True)
