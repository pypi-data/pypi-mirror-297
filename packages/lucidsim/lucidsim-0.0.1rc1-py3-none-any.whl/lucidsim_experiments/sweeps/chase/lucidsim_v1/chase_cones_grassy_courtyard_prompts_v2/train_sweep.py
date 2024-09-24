from params_proto.hyper import Sweep
from pathlib import Path

from behavior_cloning.train import TrainCfg
from lucidsim_analysis import RUN

with Sweep(RUN, TrainCfg) as sweep:
    TrainCfg.teacher_checkpoint = "/lucid-sim/lucid-sim/baselines/launch_gains/2024-03-20/04.03.35/go1/300/20/0.5/checkpoints/model_last.pt"

    TrainCfg.image_type = "augmented"
    TrainCfg.crop_image_size = None
    TrainCfg.train_yaw = True

    TrainCfg.n_epochs = 250
    TrainCfg.checkpoint_interval = 50

    with sweep.product:
        TrainCfg.dataset_prefix = [
            "lucidsim/lucidsim/corl/lucidsim_datasets/chase_cones_grassy_courtyard_prompts_v2",
        ]

        with sweep.zip:
            TrainCfg.use_stacked_dreams = [True, False]
            TrainCfg.stack_size = [5, 1]


@sweep.each
def tail(RUN, TrainCfg, *_):
    RUN.prefix, RUN.job_name, _ = RUN(
        script_path=__file__,
        job_name=f"{Path(TrainCfg.dataset_prefix).stem}/{TrainCfg.stack_size}/{TrainCfg.seed}",
    )


sweep.save(f"{Path(__file__).stem}.jsonl")
