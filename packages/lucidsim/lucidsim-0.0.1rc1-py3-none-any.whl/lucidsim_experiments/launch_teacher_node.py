if __name__ == "__main__":
    import jaynes
    from lucidsim.traj_samplers.worker_nodes.teacher_node import entrypoint
    from zaku import TaskQ

    if False:
        weaver_queue = TaskQ(name=f"{TaskQ.ZAKU_USER}:lucidsim:weaver-queue-1")
        weaver_queue.clear_queue()

        weaver_queue.add({"$kill": True})

    ip_list = [
        "vision03.csail.mit.edu",
        "vision04.csail.mit.edu",
        "vision05.csail.mit.edu",
        "vision06.csail.mit.edu",
    ]

    if False:
        weaver_queue = TaskQ(name=f"{TaskQ.ZAKU_USER}:lucidsim:weaver-queue-1")
        weaver_queue.clear_queue()

        weaver_queue.add({"$kill": True})

    for ip in ip_list:
        for gpu in range(4):
            for _ in range(2):
                jaynes.config(
                    mode="torch",
                    launch=dict(ip=ip),
                    runner=dict(
                        shell="/bin/bash --norc",
                        # shell="screen -S $USER-weaver -dm /bin/bash --norc",
                        # entry_script="nohup python -u -m jaynes.entry",
                        # shell="screen -dm nohup /bin/bash --norc",
                        envs=f"CUDA_VISIBLE_DEVICES={gpu} MUJOCO_EGL_DEVICE_ID={gpu}",
                    ),
                )
                jaynes.add(
                    entrypoint,
                    queue_name=f"{TaskQ.ZAKU_USER}:lucidsim:teacher-queue-1",
                    weaver_queue_name=f"{TaskQ.ZAKU_USER}:lucidsim:weaver-queue-1",
                )
        jaynes.execute()

    jaynes.listen()
