from collections import defaultdict

import numpy as np
import pandas as pd
from cmx import doc
from ml_logger import ML_Logger

if __name__ == "__main__":
    colors = ["#23aaff", "#ff7575", "#66c56c", "#f4b247"]

    with doc @ """# Baselines Compared to Previous Implementation""":
        loader = ML_Logger(prefix="/lucidsim/lucidsim/lucidsim_analysis/corl_analysis")


    def aggregate(*keys):
        terrains = ["stairs", "parkour", "gaps", "hurdle"]
        x_displacement_results = defaultdict(list)
        frac_goals_reached_results = defaultdict(list)
        for key in keys:
            for terrain in terrains:
                result_files = loader.glob(f"{key}_sweep/{terrain}/**/results*.pkl")

                frac_goals_reached = []
                x_displacement = []

                for fname in result_files:
                    metrics, = loader.load_pkl(fname)
                    frac_goals_reached.append(metrics["frac_goals_reached"])
                    x_displacement.append(metrics["x_displacement"])

                x_displacement_results[key].append(np.mean(x_displacement))
                frac_goals_reached_results[key].append(np.mean(frac_goals_reached))

            x_displacement_df = pd.DataFrame.from_dict(x_displacement_results, orient='index', columns=terrains)
            frac_goals_reached_df = pd.DataFrame.from_dict(frac_goals_reached_results, orient='index', columns=terrains)

        return x_displacement_df, frac_goals_reached_df


    doc @ """
    How the experiment is setup, how many seeds (for the policy), how many episodes for averaging, etc.
    """
    with doc:

        x_displacement_df, frac_goals_reached_df = aggregate("expert", "depth")

        doc.print("===== Frac Goals Reached =====")
        doc.print(frac_goals_reached_df)

        print()

        doc.print("===== X Displacement =====")
        doc.print(x_displacement_df)
