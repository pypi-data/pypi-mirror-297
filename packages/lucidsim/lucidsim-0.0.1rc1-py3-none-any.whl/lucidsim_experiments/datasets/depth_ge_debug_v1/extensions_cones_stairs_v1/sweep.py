import random

from params_proto.hyper import Sweep

from lucidsim.traj_samplers.unroll_stream import Unroll_stream as Unroll_s
from lucidsim.traj_samplers.worker_nodes.depth_teacher_node import DepthTeacherNode
from lucidsim_experiments import RUN

if __name__ == "__main__":
    from ml_logger import logger
    from cmx import doc

    doc.config("README.md")

    with doc:
        checkpoint_values = []

        expert_ckpt = "/lucid-sim/lucid-sim/baselines/launch_gains/2024-03-20/04.03.35/go1/300/20/0.5/checkpoints/model_last.pt"
        intermediate = "/lucid-sim/lucid-sim/baselines/launch_intermediate_ckpts_v3/go1/delay_4"

        all_steps = []
        with logger.Prefix(intermediate):
            checkpoint_paths = logger.glob("**/checkpoints/*.pt")

        intermediate_ckpts = [f"{intermediate}/{p}" for p in checkpoint_paths]

    doc @ f"""
    Total Number of checkpoints is {len(checkpoint_paths)}..
    """
    with doc:
        random.shuffle(checkpoint_paths)
        checkpoint_paths = checkpoint_paths[: len(checkpoint_paths)]
        checkpoint_paths += [expert_ckpt] * (len(checkpoint_paths))

    doc.print(f"in total {len(checkpoint_paths)}")

    with doc:

        def sweep_maker(short_name, checkpoint_paths, *, start=0, teacher_type, file_name):
            n = len(checkpoint_paths)
            with Sweep(RUN, Unroll_s, DepthTeacherNode) as sweep:
                Unroll_s.render = True
                Unroll_s.stop_after_termination = True

                Unroll_s.env_name = f"Extensions-cones-{short_name}-render_depth-v1"
                DepthTeacherNode.data_prefix = (
                    f"/lucidsim/lucidsim/datasets/unrolls/depth_ge_debug_v1/extensions_cones_{short_name}/{teacher_type}"
                )

                with sweep.zip:
                    Unroll_s.checkpoint = checkpoint_paths
                    Unroll_s.seed = range(start, start + n)
                    Unroll_s.rollout_id = [f"{i:04d}" for i in range(start, start + n)]

            @sweep.each
            def tail(RUN: RUN, Unroll_s: Unroll_s, DepthTeacherNode: DepthTeacherNode):
                RUN.prefix, RUN.job_name, _ = RUN(script_path=__file__, job_name=Unroll_s.env_name)

            if file_name:
                sweep.save(file_name)
                return start + len(sweep)

        for short_name in ["stairs_bcs", "stairs_wh", "stairs"]:
            for i in range(4):
                # here are the gaps many
                last = sweep_maker(
                    short_name,
                    intermediate_ckpts,
                    teacher_type=f"intermediate/collection-{i:02d}",
                    file_name=f"{short_name}_intermediate_{i}.jsonl",
                )

            # here are the gaps one
            for i in range(4):
                last = sweep_maker(
                    short_name,
                    [expert_ckpt] * 500,
                    start=last,
                    teacher_type=f"expert/collection-{i:02d}",
                    file_name=f"{short_name}_expert_{i}.jsonl",
                )
