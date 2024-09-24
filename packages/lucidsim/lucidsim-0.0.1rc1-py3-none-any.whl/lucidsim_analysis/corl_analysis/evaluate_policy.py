from lucidsim.traj_samplers import unroll

# @alan add the eval script here.

unroll.main(
    env_name="Hurdle-depth-v1",
    checkpoint="/lucid-sim/lucid-sim/baselines/launch_gains/2024-03-20/04.03.35/go1/300/20/0.5/checkpoints/model_last.pt",
    vision_key="depth",
    render=True,
    num_steps=400,
    delay=1,
)
