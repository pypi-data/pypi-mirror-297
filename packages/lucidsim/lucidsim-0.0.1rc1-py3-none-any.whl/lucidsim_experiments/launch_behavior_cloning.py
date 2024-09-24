from ml_logger.job import instr
from params_proto.hyper import Sweep

from lucidsim_analysis import RUN
from lucidsim_experiments.behavior_cloning.config import TrainCfg
from lucidsim_experiments.behavior_cloning.train import main

machines = [
    dict(ip="isola-2080ti-2.csail.mit.edu", gpu_id=7),
    dict(ip="isola-2080ti-2.csail.mit.edu", gpu_id=7),
    dict(ip="isola-2080ti-2.csail.mit.edu", gpu_id=7),
    dict(ip="isola-2080ti-2.csail.mit.edu", gpu_id=7),
]

if __name__ == "__main__":
    import jaynes

    sweep = Sweep(RUN, TrainCfg).load("sweeps/bc_sweep.jsonl")

    for machine, deps in zip(machines, sweep):
        host = machine["ip"]
        visible_devices = f'{machine["gpu_id"]}'

        jaynes.config(mode="local")
        # jaynes.config(
        #     launch=dict(ip=host),
        #     runner=dict(
        #         envs=f"CUDA_VISIBLE_DEVICES={visible_devices} MUJOCO_EGL_DEVICE_ID={visible_devices}",
        #     ),
        #     verbose=True,
        # )

        thunk = instr(main, deps)
        jaynes.run(thunk)

    # jaynes.execute()
    jaynes.listen(300)
