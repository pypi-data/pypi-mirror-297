"""
Setup a simple funciton that takes the config and pumps the
data in to a queue.

Usage: We will call this from a different launch script that
scales this up on the cluster

1. setup the sweep here (use paramsproto, think of the right way)
2. add the
"""

from params_proto import PrefixProto
from zaku import TaskQ


class DataArgs(PrefixProto):
    # queue_name = "lucidsim:weaver-queue-1"
    queue_name = "alanyu:lucidsim:eval-worker-queue-1"
    queue_name = "alanyu:lucidsim:flow-teacher-queue-1"
    # queue_name = "alanyu:lucidsim:weaver-queue-1"


def entrypoint():
    # from dotenv import load_dotenv

    # load_dotenv()
    
    queue = TaskQ(name=DataArgs.queue_name)

    queue.clear_queue()

    for _ in range(100):
        queue.add({"$kill": True})
    # # 
    # from time import sleep
    # 
    # sleep(100)
    # 
    # queue.clear_queue()


if __name__ == "__main__":
    entrypoint()
