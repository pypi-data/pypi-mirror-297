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

    depth_queue = TaskQ(name=f"{TaskQ.ZAKU_USER}:lucidsim:depth-teacher-queue-1")

    sweep_paths = """
    parkour_close_expert_0.jsonl
    parkour_close_expert_1.jsonl
    parkour_close_expert_2.jsonl
    parkour_close_expert_3.jsonl
    parkour_close_intermediate_0.jsonl
    parkour_close_intermediate_1.jsonl
    parkour_close_intermediate_2.jsonl
    parkour_close_intermediate_3.jsonl
    parkour_spread_expert_0.jsonl
    parkour_spread_expert_1.jsonl
    parkour_spread_expert_2.jsonl
    parkour_spread_expert_3.jsonl
    parkour_spread_intermediate_0.jsonl
    parkour_spread_intermediate_1.jsonl
    parkour_spread_intermediate_2.jsonl
    parkour_spread_intermediate_3.jsonl
    """.split("\n")

    # uploaded
    sweep = []

    for p in sweep_paths:
        p = p.strip()
        if p:
            sweep += Sweep.read(p)

    if input(f"Total number of jobs: {len(sweep)}, press y to confirm") == "y":
        if input("clear the queue? press y to confirm") == "y":
            depth_queue.clear_queue()
            print(depth_queue.name + "queue is cleared.")

        for deps in tqdm(sweep):
            depth_queue.add(deps)


if __name__ == "__main__":
    upload()
