"""
Launch workers and add jobs to queue
"""

from params_proto.hyper import Sweep
from zaku import TaskQ

from lucidsim.traj_samplers.unroll import Unroll, main
from lucidsim_analysis import RUN

machines = [
    dict(ip="isola-2080ti-2.csail.mit.edu", gpu_id=0),
    dict(ip="isola-2080ti-2.csail.mit.edu", gpu_id=1),
    dict(ip="isola-2080ti-2.csail.mit.edu", gpu_id=2),
    dict(ip="isola-2080ti-2.csail.mit.edu", gpu_id=3),
    dict(ip="isola-2080ti-2.csail.mit.edu", gpu_id=0),
    dict(ip="isola-2080ti-2.csail.mit.edu", gpu_id=1),
    dict(ip="isola-2080ti-2.csail.mit.edu", gpu_id=2),
    dict(ip="isola-2080ti-2.csail.mit.edu", gpu_id=3),
    dict(ip="isola-2080ti-2.csail.mit.edu", gpu_id=0),
    dict(ip="isola-2080ti-2.csail.mit.edu", gpu_id=1),
    dict(ip="isola-2080ti-2.csail.mit.edu", gpu_id=2),
    dict(ip="isola-2080ti-2.csail.mit.edu", gpu_id=3),
]


def clear_queue():
    queue = TaskQ(name="weaver:queue-1")
    while True:
        with queue.pop() as job:
            if job is None:
                break
            print(f"Clearing job {job}")

    print("All jobs are cleared out, proceeding...")


def setup_tasks():
    queue = TaskQ(name="weaver:queue-1")

    # expert_sweep = Sweep(RUN, Unroll).load("baselines/expert_sweep.jsonl")
    # for deps in expert_sweep:
    #     queue.add(deps, key=deps["RUN.prefix"])

    depth_sweep = Sweep(RUN, Unroll).load("baselines/depth_sweep.jsonl")
    for deps in depth_sweep:
        queue.add(deps, key=deps["RUN.prefix"])


def worker():
    print("in worker")

    queue = TaskQ(name="weaver:queue-1")

    while True:
        with queue.pop() as job:
            if job is None:
                break

            main(job)

    print("All jobs are done.")


if __name__ == "__main__":
    import jaynes

    clear_queue()
    setup_tasks()

    for machine in machines:
        host = machine["ip"]
        visible_devices = f'{machine["gpu_id"]}'

        # jaynes.config(mode="local")

        jaynes.config(
            launch=dict(ip=host),
            runner=dict(
                envs=f"CUDA_VISIBLE_DEVICES={visible_devices} MUJOCO_EGL_DEVICE_ID={visible_devices}",
            ),
        )

        jaynes.add(worker)

    jaynes.execute()
    jaynes.listen()
