import numpy as np
from cmx import doc
from ml_logger import ML_Logger

doc @ """
# Expert Performance

"""
with doc:

    def get_metrics(key, scenes):
        successes, deltas, trials = [], [], []
        for scene in scenes:
            with loader.Prefix(scene):
                succ, delta_x = loader.read_metrics(
                    "frac_goals_reached",
                    "x_displacement",
                    path="episode_metrics.pkl",
                    num_bins=1,
                )
                successes.append(succ.mean()[0])
                deltas.append(delta_x.mean()[0])
                trials.append(len(succ))

        doc @ f"| {key} | {np.mean(successes):0.1%} | {np.mean(deltas):0.1%} | {np.sum(trials)} |"


with doc:
    scenes = {
        "domain-rand_soccer": [
            "domain_randomization/eval_sweep/Real-vision-chase-soccer-real_flat_01_stata_grass",
            "domain_randomization/eval_sweep/Real-vision-chase-soccer-real_flat_02_wh_evening",
            "domain_randomization/eval_sweep/Real-vision-chase-soccer-real_flat_03_stata_indoor",
        ],
        "domain-rand_basketball": [
            "domain_randomization/eval_sweep/Real-vision-chase-basketball-real_flat_01_stata_grass",
            "domain_randomization/eval_sweep/Real-vision-chase-basketball-real_flat_02_wh_evening",
            "domain_randomization/eval_sweep/Real-vision-chase-basketball-real_flat_03_stata_indoor",
        ],
        "domain-rand_cones": [
            "domain_randomization/eval_sweep/Real-vision-chase-cones-real_flat_01_stata_grass",
            "domain_randomization/eval_sweep/Real-vision-chase-cones-real_flat_02_wh_evening",
            "domain_randomization/eval_sweep/Real-vision-chase-cones-real_flat_03_stata_indoor",
        ],
        "stacked_domain-rand_soccer": [
            "domain_randomization/eval_sweep_stacked/Real-vision-5-chase-soccer-real_flat_01_stata_grass",
            "domain_randomization/eval_sweep_stacked/Real-vision-5-chase-soccer-real_flat_02_wh_evening",
            "domain_randomization/eval_sweep_stacked/Real-vision-5-chase-soccer-real_flat_03_stata_indoor",
        ],
        "stacked_domain-rand_basketball": [
            "domain_randomization/eval_sweep_stacked/Real-vision-5-chase-basketball-real_flat_01_stata_grass",
            "domain_randomization/eval_sweep_stacked/Real-vision-5-chase-basketball-real_flat_02_wh_evening",
            "domain_randomization/eval_sweep_stacked/Real-vision-5-chase-basketball-real_flat_03_stata_indoor",
        ],
        "stacked_domain-rand_cones": [
            "domain_randomization/eval_sweep_stacked/Real-vision-5-chase-cones-real_flat_01_stata_grass",
            "domain_randomization/eval_sweep_stacked/Real-vision-5-chase-cones-real_flat_02_wh_evening",
            "domain_randomization/eval_sweep_stacked/Real-vision-5-chase-cones-real_flat_03_stata_indoor",
        ],
        "expert": [
            "expert/eval_sweep/Real-heightmap-chase-real_flat_01_stata_grass",
            "expert/eval_sweep/Real-heightmap-chase-real_flat_02_wh_evening",
            "expert/eval_sweep/Real-heightmap-chase-real_flat_03_stata_indoor",
        ],
    }

    prefix = "/lucidsim/lucidsim/corl_experiments/sweeps/chase"
    loader = ML_Logger(prefix=prefix)

    with doc.hide:
        doc @ """
    **Expert**

    | Scene | Goals Reached | X Displacement | Num Trials
    | ------- | ------------- | -------------- | ---------- |"""

    for scene in scenes:
        get_metrics(scene, scenes[scene])

    doc.flush()
