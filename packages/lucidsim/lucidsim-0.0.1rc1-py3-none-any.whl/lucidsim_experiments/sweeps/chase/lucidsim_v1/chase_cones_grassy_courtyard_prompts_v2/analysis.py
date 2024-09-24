from cmx import doc
from ml_logger import ML_Logger

doc @ """
# Expert Performance

"""
with doc:
    def get_metrics(scene):
        with loader.Prefix(scene):
            print(loader.get_dash_url())
            succ, delta_x = loader.read_metrics(
                "frac_goals_reached",
                "x_displacement",
                path="episode_metrics.pkl",
                num_bins=1,
            )

        doc @ f"| {scene} | {succ.mean()[0]:0.1%} | {delta_x.mean()[0]:0.1%} | {len(succ)} |"

with doc:
    scenes = [
        "chase_cones_grassy_courtyard_prompts_v2/eval_sweep/Real-vision-chase-cones-real_flat_01_stata_grass",
        "chase_cones_grassy_courtyard_prompts_v2/eval_sweep/Real-vision-5-chase-cones-real_flat_01_stata_grass"
    ]

    prefix = "/lucidsim/lucidsim/corl_experiments/sweeps/chase/lucidsim_v1"
    loader = ML_Logger(prefix=prefix)

with doc.hide:
    doc @ """
    **Expert**

    | Scene | Goals Reached | X Displacement | Num Trials
    | ------- | ------------- | -------------- | ---------- |"""

    for scene in scenes:
        get_metrics(scene)

doc.flush()
