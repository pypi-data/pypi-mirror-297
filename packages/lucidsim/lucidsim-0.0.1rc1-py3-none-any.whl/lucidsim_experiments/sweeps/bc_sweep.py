from params_proto.hyper import Sweep
from pathlib import Path

from lucidsim_analysis import RUN
from lucidsim_experiments.behavior_cloning.config import TrainCfg

with Sweep(RUN, TrainCfg) as sweep:
    TrainCfg.expert_ckpt = "/lucid-sim/lucid-sim/baselines/launch_gains/2024-03-20/04.03.35/go1/300/20/0.5"
    TrainCfg.image_type = "augmented"
    TrainCfg.trajectories_per_scene = [[0]]
    TrainCfg.val_trajectories_per_scene = [[0]]
    TrainCfg.val_scenes = None

    with sweep.zip:
        TrainCfg.scenes = [
            ["alan_debug_train/gaps/scene_00001"],
            ["alan_debug_train/hurdle/scene_00001"],
            ["alan_debug_train/stairs/scene_00001"],
            ["alan_debug_train/parkour/scene_00001"],
        ]
        TrainCfg.val_scenes = [
            ["alan_debug_train/gaps/scene_00001"],
            ["alan_debug_train/hurdle/scene_00001"],
            ["alan_debug_train/stairs/scene_00001"],
            ["alan_debug_train/parkour/scene_00001"],
        ]

    TrainCfg.n_epochs = 500


@sweep.each
def tail(RUN, TrainCfg, *_):
    RUN.prefix, RUN.job_name, _ = RUN(
        script_path=__file__,
        job_name=f"{TrainCfg.scenes[0]}/{TrainCfg.image_type}/{TrainCfg.seed}",
    )


sweep.save(f"{Path(__file__).stem}.jsonl")
