""" This program tests the sandpile grid for scale invariance.
Scale invariance means that the structure of the observables and grid is
(roughly) unchanged to changes in the dimensions of the grid.
"""

""" IMPORTS """
import numpy as np
import sys
import matplotlib.pyplot as plt

sys.path.append("./core")
import sandpile

from importlib import reload
reload(sandpile)

import main as main_script


""" INPUTS """
dimensions = [2, 5, 10, 50, 100]


""" FUNCTIONS """
def main():
    # Directory to save output plots.
    dir = "./../output/scale_invariance/"

    # Create a histogram of an observable for different grid dimensions.
    for lw in dimensions:
        sp = sandpile.SandPile(lw, lw)

        for i in range(10000):
            main_script.execute_avalanches(sp)

        fname = f"{dir}stats.pik"
        sp.save_avalanche_stats(fname)

        ob = sandpile.Observables(fname)
        ob.histogram(ob.topples, density=0)
        plt.savefig(f"{dir}histogram_{lw}.png")


""" EXECUTION """
if __name__ == "__main__":
    main()
