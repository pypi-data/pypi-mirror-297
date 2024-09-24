from params_proto.hyper import Sweep
from pathlib import Path

from lucidsim.traj_samplers.unroll import Unroll
from lucidsim_experiments import RUN

if __name__ == "__main__":
    with Sweep(RUN, Unroll) as sweep:
        Unroll.render = False
        Unroll.log_metrics = True
        Unroll.num_steps = 300
        Unroll.vision_key = "vision"

        with sweep.product:
            with sweep.chain:
                with sweep.product:
                    Unroll.env_name = [
                        "Real-vision-chase-cones-real_flat_01_stata_grass",
                        # "Real-vision-chase-cones-real_flat_02_wh_evening",
                        # "Real-vision-chase-cones-real_flat_03_stata_indoor",
                    ]
                    Unroll.checkpoint = [
                        "/lucidsim/lucidsim/lucidsim_analysis/corl_analysis/train_sweep/chase_cones_grassy_courtyard_prompts_v2/1/100/checkpoints/net_last.pt"
                    ]

                with sweep.product:
                    Unroll.env_name = [
                        "Real-vision-5-chase-cones-real_flat_01_stata_grass",
                        # "Real-vision-5-chase-cones-real_flat_02_wh_evening",
                        # "Real-vision-5-chase-cones-real_flat_03_stata_indoor",
                    ]
                    Unroll.checkpoint = [
                        "/lucidsim/lucidsim/lucidsim_analysis/corl_analysis/train_sweep/chase_cones_grassy_courtyard_prompts_v2/5/100/checkpoints/net_last.pt"
                    ]

            Unroll.seed = [*range(50)]

    @sweep.each
    def tail(RUN, Unroll):
        RUN.prefix, RUN.job_name, _ = RUN(
            script_path=__file__,
            job_name=f"{Unroll.env_name}",
        )
        print(RUN.prefix)

    sweep.save(f"{Path(__file__).stem}.jsonl")
