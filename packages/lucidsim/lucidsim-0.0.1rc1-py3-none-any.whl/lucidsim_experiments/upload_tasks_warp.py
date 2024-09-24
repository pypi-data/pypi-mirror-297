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
    from tqdm import tqdm

    # load_dotenv()

    sweep = Sweep.read("datasets/lucidsim_v1/extension_stairs_wh_cones_gpt_prompts_v2_filtered/sweep/warp_7.jsonl")

    # queue = TaskQ(name=f"{TaskQ.ZAKU_USER}:lucidsim:teacher-queue-1")
    # eval_queue = TaskQ(name=f"{TaskQ.ZAKU_USER}:lucidsim:eval-worker-queue-1")
    # weaver_queue = TaskQ(name=f"{TaskQ.ZAKU_USER}:lucidsim:weaver-queue-1")
    warp_queue = TaskQ(name=f"{TaskQ.ZAKU_USER}:lucidsim:warping-queue-1")

    # queue.clear_queue()
    # eval_queue.clear_queue()
    # weaver_queue.clear_queue()
    warp_queue.clear_queue()

    # queue = TaskQ(name=f"{TaskQ.ZAKU_USER}:lucidsim:dr-teacher-queue-1")

    for deps in tqdm(sweep):
        warp_queue.add(deps)
        # break

    print("finished uploading")


if __name__ == "__main__":
    upload()
