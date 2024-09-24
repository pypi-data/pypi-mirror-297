from params_proto.hyper import Sweep

from lucidsim_experiments.dagger_runner import main

if __name__ == "__main__":
    # sweep = Sweep.read("extensions_hurdle_cone_combined_prompts_v1-alan-flow_7/sweep/sweep.jsonl")
    # sweep = Sweep.read("extensions_parkour_cones_close_pillar-combined_prompts_v1/sweep/sweep.jsonl")
    # sweep = Sweep.read("extensions_parkour_cones_spread_pillar-combined_prompts_v1/sweep/sweep.jsonl")

    # sweep = Sweep.read("extensions_cones_stairs_wh-bcs_prompts_v7_v1/sweep/sweep.jsonl")
    # sweep = Sweep.read("extensions_cones_stairs_wh-bcs_prompts_v7_v1/sweep_v2/sweep.jsonl")

    # sweep = Sweep.read("extensions_hurdle_cone_combined_prompts_v1-alan-flow_7/sweep_nostack/sweep.jsonl")
    # sweep = Sweep.read("extensions_hurdle_many_combined_prompts_realsense_v1/sweep/sweep.jsonl")

    # sweep = Sweep.read("extensions_hurdle_cone_combined_prompts_v1/sweep_more_expert/sweep.jsonl")
    # sweep = Sweep.read("extensions_cones_stairs_wh-bcs_prompts_v7_v1/sweep_more_expert/sweep.jsonl")

    # sweep = Sweep.read("extensions_hurdle_cone_combined_prompts_v1/sweep_no_cobble/sweep.jsonl")
    # sweep = Sweep.read("extensions_hurdle_cone_combined_prompts_v1/sweep_only_cobble/sweep.jsonl")
    # sweep = Sweep.read("extensions_hurdle_cone_combined_prompts_v1/sweep_only_lab/sweep.jsonl")
    sweep = Sweep.read("extensions_cones_stairs_wh-bcs_prompts_v7_v1/sweep_fixed_bug/sweep.jsonl")

    for job in sweep:
        main(
            job,
            # debug=True,
            # dagger_start=1,
        )
