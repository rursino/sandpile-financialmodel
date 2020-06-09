""" This program tests the sandpile grid for scale invariance.
Scale invariance means that the structure of the observables and grid is
(roughly) unchanged to changes in the dimensions of the grid.
"""

""" IMPORTS """
from time import sleep
import numpy as np
import sys
import matplotlib.pyplot as plt

sys.path.append("./core")
import sandpile

from importlib import reload
reload(sandpile)

import main as main_script


""" INPUTS """
dimensions = [2, 5, 10, 20]

# Directory to save output plots.
dir = "./../output/scale_invariance/"


""" FUNCTIONS """
def main():

    print("\n"+"="*30)
    print("SCALE_INVARIANCE.PY: TESTING SCALE INVARIANCE FROM MANY AVALANCHES")
    print("="*30+"\n\n")
    sleep(1)

    # Create a histogram of an observable for different grid dimensions.
    print("Performing scale invariances for dimensions 2, 5, 10, 50, 100.")
    print("\n"+"-"*30+"\n")
    for lw in dimensions:
        sp = sandpile.SandPile(lw, lw)

        print(f"Executing 5000 avalanches on sandpile with dimensions {lw}, {lw}")
        for i in range(5000):
            main_script.execute_avalanches(sp, i)

        fname = f"{dir}stats.pik"
        sp.save_avalanche_stats(fname)
        ob = sandpile.Observables(fname)

        print(f"\n\nDone! Saving powerlaw fit plot to {fname}")
        ob.powerlaw_fit(ob.topples, plot=1, xscale="log", yscale="log")
        plt.xlabel("Topples")
        plt.ylabel("Probability")
        plt.title(f"Powerlaw Fit, Dimensions: {lw}")
        plt.savefig(f"{dir}powerlaw_fit{lw}.png")

        print("\nPlot saved! Moving on to the next sandpile...")

    print("\n"+"-"*30+"\n")
    print("Program finished!")


""" EXECUTION """
if __name__ == "__main__":
    main()
