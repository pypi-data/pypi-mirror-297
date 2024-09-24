if __name__ == "__main__":
    import jaynes
    from lucidsim.traj_samplers.worker_nodes.depth_teacher_node import entrypoint
    from ml_logger.job import instr
    from zaku import TaskQ

    ips = {
        "isola-2080ti-1.csail.mit.edu": [0, 1, 2, 3] * 5,
        # "isola-2080ti-2.csail.mit.edu": [0, 1, 2, 3] * 10,
        "isola-2080ti-3.csail.mit.edu": [0, 1, 2, 3] * 5,
        "isola-2080ti-4.csail.mit.edu": [0, 1, 2, 3] * 5,
        # "freeman-titanrtx-1.csail.mit.edu": [0, 1, 2, 3, 4, 5, 6, 7] * 12,
        # "vision20": [1, 2, 3, 4, 5, 6, 7] * 12,
    }

    # # this sets the default loging server here and in the job.
    # import os
    # RUN.server = os.environ["WEAVER_DATA_SERVER"]

    for ip, gpus in ips.items():
        for gpu in gpus:
            host = ip
            visible_devices = f"{gpu}"

            envs = f"CUDA_VISIBLE_DEVICES={visible_devices} MUJOCO_EGL_DEVICE_ID={visible_devices}"
            jaynes.config(
                mode="torch",
                launch=dict(ip=host),
                runner=dict(
                    envs=envs,
                    # shell="screen -dm /bin/bash --norc",
                ),
            )

            thunk = instr(
                entrypoint,
                queue_name=f"{TaskQ.ZAKU_USER}:lucidsim:depth-teacher-queue-1",
                __diff=False,
            )
            jaynes.add(thunk)

        jaynes.execute()
    jaynes.listen()
