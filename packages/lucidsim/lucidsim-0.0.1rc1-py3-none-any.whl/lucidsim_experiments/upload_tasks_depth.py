"""


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
from zaku import TaskQ


def upload():
    # from dotenv import load_dotenv
    from tqdm import tqdm

    # load_dotenv()

    # we use the Sweep.read function to load the jsonl.
    # sweep = Sweep.read("datasets/depth_v1/chase_cones_v1/sweep.jsonl")
    # sweep += Sweep.read("datasets/depth_v1/chase_soccer_v1/sweep.jsonl")

    sweep = Sweep.read("datasets/depth_v1/extensions_cones_stairs_wh_v4/sweep.jsonl")

    queue = TaskQ(name=f"{TaskQ.ZAKU_USER}:lucidsim:depth-teacher-queue-1")
    queue.clear_queue()
    for deps in tqdm(sweep):
        queue.add(deps)
        # break

    print("finished uploading")


if __name__ == "__main__":
    upload()
