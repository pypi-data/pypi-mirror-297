queues = [
    # "alanyu:lucidsim:flow-teacher-queue-1",
    # "alanyu:lucidsim:flow-teacher-queue-1.return-queue",
    "alanyu:lucidsim:flow-teacher-queue-2",
    "alanyu:lucidsim:flow-teacher-queue-2.return-queue",
    "alanyu:lucidsim:weaver-queue-1",
    "alanyu:lucidsim:trainer-queue-1",
    "alanyu:lucidsim:trainer-queue-2",
    # "alanyu:lucidsim:flow-teacher-queue-3",
    # "alanyu:lucidsim:flow-teacher-queue-3.return-queue",
]
# queues = ["alanyu:lucidsim:depth-trainer-queue-1"]
print("yo")

from zaku import TaskQ

for name in queues:
    q = TaskQ(name=name)
    q.clear_queue()
    print(q.count())
