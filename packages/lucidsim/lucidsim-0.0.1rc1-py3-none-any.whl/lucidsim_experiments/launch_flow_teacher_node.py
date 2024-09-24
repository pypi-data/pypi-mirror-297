if __name__ == "__main__":
    import jaynes
    from lucidsim.traj_samplers.worker_nodes.flow_teacher_node import entrypoint
    from zaku import TaskQ

    # machine_list = Sweep.read("machine_list.jsonl")

    # machine_list = [
    #     {"ip": "vision03", "gpu_id": 0},
    #     {"ip": "vision03", "gpu_id": 1},
    #     {"ip": "vision03", "gpu_id": 2},
    #     {"ip": "vision03", "gpu_id": 3},
    #     {"ip": "vision04", "gpu_id": 0},
    #     {"ip": "vision04", "gpu_id": 1},
    #     {"ip": "vision04", "gpu_id": 2},
    #     {"ip": "vision04", "gpu_id": 3},
    #     {"ip": "vision05", "gpu_id": 0},
    #     {"ip": "vision05", "gpu_id": 1},
    #     {"ip": "vision05", "gpu_id": 2},
    #     {"ip": "vision05", "gpu_id": 3},
    #     {"ip": "vision06", "gpu_id": 0},
    #     {"ip": "vision06", "gpu_id": 1},
    #     {"ip": "vision06", "gpu_id": 2},
    #     {"ip": "vision06", "gpu_id": 3},
    # ]

    ip_list = {
        # "vision01": [0, 1, 2, 3, 4, 5, 6, 7] * 3,
        # "vision02": [0, 1, 2, 3, 4, 5, 6, 7] * 3,
        "vision03": [0, 1, 2, 3] * 3,
        "vision04": [0, 1, 2, 3] * 3,
        "vision05": [0, 1, 2, 3] * 3,
        "vision06": [0, 1, 2, 3] * 3,
        "vision07": [0, 1, 2, 3, 4, 5, 6, 7] * 3,
        "vision08": [0, 1, 2, 3] * 3,
        # "vision09": [0, 1, 2, 3, 4, 5, 6, 7] * 3,
        "vision10": [0, 1, 2, 3, 4, 5, 6, 7] * 3,
        "vision11": [0, 1, 2, 3, 4, 5, 6, 7] * 3,
        "vision12": [0, 1, 2, 3, 4, 5, 6, 7] * 3,
        # "vision13": [0, 1, 2, 3, 4, 5, 6, 7] * 2,
        "vision14": [0] * 3,
        "vision15": [0, 1] * 3,
        "vision16": [0, 1, 2, 3, 4, 5, 6] * 3,
        # "vision17": [0, 1, 2, 3, 4, 5, 6] * 3,
        # "vision18": [0, 1, 2, 3, 4, 5, 6],
        # "vision19": [0, 1, 2, 3, 4, 5, 6],
        # "vision20": [0, 1, 2, 3, 4, 5, 6],
        # "vision21": [0, 1, 2, 3, 4, 5, 6, 7] * 3,
        # "vision22": [0],
        # "vision23": [0, 1, 2, 3, 4, 5, 6, 7] * 2,
        # "vision24": [0, 1, 2, 3, 4, 5, 6, 7] * 3,
        # "vision25": [0, 1, 2, 3, 4, 5, 6, 7] * 3,
        # "vision26": [0, 1, 2, 3, 4, 5, 6, 7] * 3,
        # "vision27": [0, 1, 2, 3, 4, 5, 6, 7] * 2,
        # "vision28": [0, 1, 2, 3, 4, 5, 6, 7] * 3,
        # "vision29": [0, 1, 2, 3, 4, 5, 6, 7],
    }

    if False:
        weaver_queue = TaskQ(name=f"{TaskQ.ZAKU_USER}:lucidsim:weaver-queue-1")
        weaver_queue.clear_queue()

        weaver_queue.add({"$kill": True})

    for ip, gpus in ip_list.items():
        for gpu in gpus:
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
                queue_name=f"{TaskQ.ZAKU_USER}:lucidsim:flow-teacher-queue-1",
                weaver_queue_name=f"{TaskQ.ZAKU_USER}:lucidsim:weaver-queue-1",
            )
        jaynes.execute()

    jaynes.listen()
