from params_proto.hyper import Sweep

machines = [
    dict(ip="isola-2080ti-1.csail.mit.edu", gpu_id=0),
    dict(ip="isola-2080ti-1.csail.mit.edu", gpu_id=0),
    dict(ip="isola-2080ti-1.csail.mit.edu", gpu_id=0),
    dict(ip="isola-2080ti-1.csail.mit.edu", gpu_id=1),
    dict(ip="isola-2080ti-1.csail.mit.edu", gpu_id=1),
    dict(ip="isola-2080ti-1.csail.mit.edu", gpu_id=1),
    dict(ip="isola-2080ti-1.csail.mit.edu", gpu_id=2),
    dict(ip="isola-2080ti-1.csail.mit.edu", gpu_id=2),
    dict(ip="isola-2080ti-1.csail.mit.edu", gpu_id=2),
    dict(ip="isola-2080ti-1.csail.mit.edu", gpu_id=3),
    dict(ip="isola-2080ti-1.csail.mit.edu", gpu_id=3),
    dict(ip="isola-2080ti-1.csail.mit.edu", gpu_id=3),
    dict(ip="isola-2080ti-3.csail.mit.edu", gpu_id=0),
    dict(ip="isola-2080ti-3.csail.mit.edu", gpu_id=0),
    dict(ip="isola-2080ti-3.csail.mit.edu", gpu_id=0),
    dict(ip="isola-2080ti-3.csail.mit.edu", gpu_id=1),
    dict(ip="isola-2080ti-3.csail.mit.edu", gpu_id=1),
    dict(ip="isola-2080ti-3.csail.mit.edu", gpu_id=1),
    dict(ip="isola-2080ti-3.csail.mit.edu", gpu_id=2),
    dict(ip="isola-2080ti-3.csail.mit.edu", gpu_id=2),
    dict(ip="isola-2080ti-3.csail.mit.edu", gpu_id=2),
    dict(ip="isola-2080ti-3.csail.mit.edu", gpu_id=3),
    dict(ip="isola-2080ti-3.csail.mit.edu", gpu_id=3),
    dict(ip="isola-2080ti-3.csail.mit.edu", gpu_id=3),
    dict(ip="freeman-titanrtx-1.csail.mit.edu", gpu_id=0),
    dict(ip="freeman-titanrtx-1.csail.mit.edu", gpu_id=1),
    dict(ip="freeman-titanrtx-1.csail.mit.edu", gpu_id=2),
    dict(ip="freeman-titanrtx-1.csail.mit.edu", gpu_id=3),
    dict(ip="freeman-titanrtx-1.csail.mit.edu", gpu_id=4),
    dict(ip="freeman-titanrtx-1.csail.mit.edu", gpu_id=5),
]

if __name__ == "__main__":
    import jaynes
    from ml_logger.job import instr
    from behavior_cloning.train import main

    sweeps = [
        # "datasets/domain_randomization_5_v1/chase_cones_v1/train_sweep.jsonl",
        # "datasets/domain_randomization_5_v1/chase_soccer_v1/train_sweep.jsonl",
        "datasets/depth_v1/chase_cones_v1/train_sweep.jsonl",
        "datasets/depth_v1/chase_soccer_v1/train_sweep.jsonl",
    ]

    sweep = Sweep.read(sweeps[0])
    for s in sweeps[1:]:
        sweep += Sweep.read(s)

    print(len(sweep))

    # exit()
    for machine, deps in zip(machines, sweep):
        host = machine["ip"]
        visible_devices = f'{machine["gpu_id"]}'

        jaynes.config(mode="local")
        # jaynes.config(
        #     launch=dict(ip=host),
        #     runner=dict(
        #         # shell="/bin/bash --norc",
        #         shell="screen -dm /bin/bash --norc",
        #         envs=f"CUDA_VISIBLE_DEVICES={visible_devices} MUJOCO_EGL_DEVICE_ID={visible_devices}",
        #     ),
        #     verbose=True,
        # )

        thunk = instr(main, deps)
        # jaynes.add(thunk)
        jaynes.run(thunk)

    # jaynes.execute()
    jaynes.listen(300)
