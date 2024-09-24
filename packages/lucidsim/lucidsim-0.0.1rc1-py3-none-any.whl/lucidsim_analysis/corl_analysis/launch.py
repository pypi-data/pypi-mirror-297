from params_proto.hyper import Sweep

from lucidsim.traj_samplers.unroll import Unroll, main
from lucidsim_analysis import RUN, instr

machines = [
    dict(ip="freeman-v100-2.csail.mit.edu", gpu_id=0),
    dict(ip="freeman-v100-2.csail.mit.edu", gpu_id=0),
    dict(ip="freeman-v100-2.csail.mit.edu", gpu_id=1),
    dict(ip="freeman-v100-2.csail.mit.edu", gpu_id=1),
    dict(ip="freeman-v100-2.csail.mit.edu", gpu_id=2),
    dict(ip="freeman-v100-2.csail.mit.edu", gpu_id=2),
    dict(ip="freeman-v100-2.csail.mit.edu", gpu_id=3),
    dict(ip="freeman-v100-2.csail.mit.edu", gpu_id=3),
]

if __name__ == "__main__":
    import jaynes

    sweep = Sweep(RUN, Unroll).load("baselines/depth_sweep.jsonl")
    for machine, deps in zip(machines, sweep):
        host = machine["ip"]
        visible_devices = f'{machine["gpu_id"]}'

        # jaynes.config(mode='local')

        jaynes.config(
            launch=dict(ip=host),
            runner=dict(
                envs=f"CUDA_VISIBLE_DEVICES={visible_devices} MUJOCO_EGL_DEVICE_ID={visible_devices}",
            ),
            verbose=True,
        )

        thunk = instr(main, deps)
        jaynes.run(thunk)

    # jaynes.execute()
    jaynes.listen(300)
