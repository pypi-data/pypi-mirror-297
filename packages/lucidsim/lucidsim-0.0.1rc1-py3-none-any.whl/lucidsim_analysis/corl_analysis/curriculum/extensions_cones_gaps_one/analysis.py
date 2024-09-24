import numpy as np
from cmx import doc
from ml_logger import ML_Logger

doc @ """
# Transformer Student Performance

"""
with doc:

    def get_metrics(scene):
        with loader.Prefix(scene):
            print(loader.get_dash_url())
            succ, delta_x = loader.read_metrics(
                "frac_goals_reached",
                "x_displacement",
                path="episode_metrics.pkl",
                num_bins=1,
            )

        doc @ f"| {scene} | {succ.mean()[0]:0.1%} | {delta_x.mean()[0]:0.1%} | {len(succ)} |"

        return succ.mean()[0], delta_x.mean()[0]


with doc:
    all_scenes = []

    import matplotlib.pyplot as plt

    # Generating the values for x and yaw
    x = np.linspace(0, 4.5, 20)
    yaw = np.linspace(0, np.pi / 4, 20)

    # Placeholder for collecting success rates
    success_rates = []

    prefix = "lucidsim/lucidsim/corl_experiments/extensions_cones_gaps_one/sweep"
    loader = ML_Logger(prefix=prefix)
    # Simulate collecting success rate for each combination of x and yaw
    for xi in x:
        for yi in yaw:
            # Replace this with your actual method of obtaining the success rate
            success_rate, _ = get_metrics(f"{xi}/{yi}")
            success_rates.append(success_rate)

    # Convert the flat list of success rates to a 2D array
    success_rate_matrix = np.reshape(success_rates, (len(x), len(yaw)))

    # Create a meshgrid for plotting
    X, Y = np.meshgrid(x, yaw)

    # Plotting
    plt.figure(figsize=(10, 6))
    c = plt.pcolormesh(X, Y, success_rate_matrix, shading="auto", cmap="viridis")
    plt.colorbar(c, label="Success Rate")
    plt.xlabel("X (units)")
    plt.ylabel("Yaw (radians)")
    plt.title("Success Rate Distribution")
    plt.show()

doc.flush()
