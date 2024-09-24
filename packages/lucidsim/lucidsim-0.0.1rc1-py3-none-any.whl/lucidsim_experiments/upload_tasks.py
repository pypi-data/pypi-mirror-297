"""
for uploading tasks to the queue.


# this is for killing jobs


from zaku import TaskQ
queue = TaskQ(name="lucidsim:eval-worker-queue-1", uri="http://escher.csail.mit.edu:8100")
queue.clear_queue()

for i in range(10):
    deps = {"$kill": True}
    queue.add(deps)

queue.clear_queue()

"""

from params_proto.hyper import Sweep
from tqdm import tqdm
from zaku import TaskQ


# class Upload(ParamsProto):
#     queue_name: Literal["depth", "flow"] = ""
#     sweep = ""


def upload():
    assert TaskQ.ZAKU_USER, "ZAKU_USER needs to be set for this upload."

    # depth_queue = TaskQ(name=f"{TaskQ.ZAKU_USER}:lucidsim:depth-teacher-queue-1")
    # depth_queue.clear_queue()
    #
    # sweep_paths = """
    # gaps_many_expert_0.jsonl
    # gaps_many_expert_1.jsonl
    # gaps_many_intermediate_0.jsonl
    # gaps_many_intermediate_1.jsonl
    # gaps_one_expert_0.jsonl
    # gaps_one_expert_1.jsonl
    # gaps_one_intermediate_0.jsonl
    # gaps_one_intermediate_1.jsonl
    # gaps_many_expert_2.jsonl
    # gaps_many_expert_3.jsonl
    # gaps_many_intermediate_2.jsonl
    # gaps_many_intermediate_3.jsonl
    # gaps_one_expert_2.jsonl
    # gaps_one_expert_3.jsonl
    # gaps_one_intermediate_2.jsonl
    # gaps_one_intermediate_3.jsonl
    # """.split("\n")
    #
    # # uploaded
    #
    # sweep = []
    # for p in sweep_paths:
    #     if p.strip():
    #         sweep += Sweep.read("datasets/depth_ge_debug_v1/extensions_cones_gaps_v1/" + p.strip())
    #
    # if input(f"Total number of jobs: {len(sweep)}, press y to confirm") == "y":
    #
    #     if input(f"clear the queue? press y to confirm") == 'y':
    #         depth_queue.clear_queue()
    #         print(depth_queue.name + "queue is cleared.")
    #
    #     for deps in tqdm(sweep):
    #         depth_queue.add(deps)

    # sweep = Sweep.read("datasets/lucidsim_v1/extensions_hurdle_man")
    # queue = TaskQ(name="alanyu:lucidsim:depth-teacher-queue-1")
    queue = TaskQ(name="alanyu:lucidsim:eval-worker-queue-1")
    # queue.clear_queue()
    # sweep = Sweep.read("analysis/stairs_cones/sweep/eval_sweep_depth_realsense.jsonl")
    # sweep = Sweep.read("analysis/hurdle_cones/sweep/eval_sweep_lucidsim_nodim.jsonl")

    # sweep = Sweep.read("analysis/stairs_cones/sweep/eval_sweep_lucidsim_v2.jsonl")
    # sweep = Sweep.read("analysis/hurdle_cones/sweep/eval_sweep_lucidsim_more_expert.jsonl")
    # sweep = Sweep.read("datasets/lucidsim_v1/extensions_hurdle_cone_cobblestone_prompts_v1-alan-flow_7/sweep/eval_sweep_v2.jsonl")
    # sweep = Sweep.read("analysis/chase_soccer/sweep/eval_sweep_depth_realsense.jsonl")[1:]
    # sweep += Sweep.read("analysis/chase_cones/sweep/eval_sweep_depth_realsense.jsonl")[1:]

    # sweep = Sweep.read("analysis/hurdle_cones/sweep/eval_sweep_lucidsim_only_cobble_v2.jsonl")
    # sweep = Sweep.read("analysis/hurdle_cones/sweep/eval_sweep_lucidsim_no_cobble_v2.jsonl")
    sweep = Sweep.read("analysis/hurdle_cones/sweep/eval_sweep_lucidsim_only_lab.jsonl")

    # sweep = Sweep.read("analysis/stairs_cones/sweep/eval_sweep_lucidsim_fix_bug.jsonl")

    # queue.clear_queue()
    queue.clear_queue()
    print("Total number of jobs:", len(sweep))
    for deps in tqdm(sweep):
        queue.add(deps)
    #     break


if __name__ == "__main__":
    upload()
