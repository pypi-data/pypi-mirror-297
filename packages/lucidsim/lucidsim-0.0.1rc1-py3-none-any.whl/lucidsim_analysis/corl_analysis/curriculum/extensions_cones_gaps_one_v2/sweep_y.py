import json
from pathlib import Path

import numpy as np

from lucidsim_experiments import RUN

if __name__ == "__main__":
    with open(f"{Path(__file__).stem}.jsonl", "w") as f:
        deps = []
        for seed in range(10):
            for x in np.linspace(0, 4.5, 20):
                for y in np.linspace(-0.25, 0.25, 20):
                    prefix, job_name, *_ = RUN(
                        script_path=__file__,
                        job_name=f"{x}/{y}",
                    )
                    job = {
                        "unroll.render": False,
                        "unroll.log_metrics": True,
                        "unroll.num_steps": 700,
                        "unroll.vision_key": None,
                        "unroll.env_name": "Extensions-cones-gaps_one-heightmap-v1",
                        "unroll.checkpoint": "/lucid-sim/lucid-sim/baselines/launch_intermediate_ckpts_v3/go1/delay_4/300/checkpoints/model_last.pt",
                        "spawn_pose": (x, y, 0.448, 0),
                        "unroll.seed": seed,
                        "RUN.prefix": prefix,
                    }

                    deps.append(job)

                    f.write(json.dumps(job) + "\n")

        print(f"Saved {len(deps)} jobs to {f.name}")
