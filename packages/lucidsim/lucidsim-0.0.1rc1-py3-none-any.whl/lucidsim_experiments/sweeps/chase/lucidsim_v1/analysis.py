import numpy as np
from cmx import doc
from ml_logger import ML_Logger

doc @ """
# Chase Cones: Comparison with Domain Randomization Baseline

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

        doc @ f"| {key} | {np.mean(successes):0.1%} | {np.mean(deltas):0.1%} |" #  {np.sum(trials)} |"


with doc:
    scenes = {
        "expert": [
            "expert/eval_sweep/Real-heightmap-chase-real_flat_01_stata_grass",
            "expert/eval_sweep/Real-heightmap-chase-real_flat_02_wh_evening",
        ],
        "domain-rand_cones": [
            "domain_randomization/eval_sweep/Real-vision-chase-cones-real_flat_01_stata_grass",
            "domain_randomization/eval_sweep/Real-vision-chase-cones-real_flat_02_wh_evening",
        ],
        "inconsistent_stacked_domain-rand_cones": [
            "domain_randomization/eval_sweep_stacked/Real-vision-5-chase-cones-real_flat_01_stata_grass",
            "domain_randomization/eval_sweep_stacked/Real-vision-5-chase-cones-real_flat_02_wh_evening",
        ],
        "lucidsim_cones": [
            "lucidsim_v1/chase_cones_grassy_courtyard_prompts_v2/eval_sweep/Real-vision-chase-cones-real_flat_01_stata_grass",
            "lucidsim_v1/chase_cones_red_brick_courtyard_prompts_v4/eval_sweep/Real-vision-chase-cones-real_flat_02_wh_evening",
        ],
        "inconsistent_stacked_lucidsim_cones": [
            "lucidsim_v1/chase_cones_grassy_courtyard_prompts_v2/eval_sweep/Real-vision-5-chase-cones-real_flat_01_stata_grass",
            "lucidsim_v1/chase_cones_red_brick_courtyard_prompts_v4/eval_sweep/Real-vision-5-chase-cones-real_flat_02_wh_evening",
        ],
    }

    prefix = "/lucidsim/lucidsim/corl_experiments/sweeps/chase"
    loader = ML_Logger(prefix=prefix)

    with doc.hide:
        doc @ """
    **Metrics for the cone chasing task. We evaluate each agent on two (three) real scenes with 50 seeds each. LucidSim agents are trained on prompt collections tailored to the scene type.** 

    | Scene | Goals Reached | X Displacement |
    | ------- | ------------- | -------------- |"""

    for scene in scenes:
        get_metrics(scene, scenes[scene])

    doc.flush()
