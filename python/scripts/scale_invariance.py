""" This program tests the sandpile grid for scale invariance.
Scale invariance means that the structure of the observables and grid is
(roughly) unchanged to changes in the dimensions of the grid.
"""

import numpy as np
import sys
import matplotlib.pyplot as plt

sys.path.append("./core")
import sandpile

from importlib import reload
reload(sandpile)

import main as main_script

""" INPUTS """
dimensions = [5, 10, 100, 1000, 10000]


""" FUNCTIONS """
def fn():
    raise NotImplementedError()

def main():
    for lw in dimensions:
        sp = sandpile.SandPile(lw, lw)

        for i in range(10000):
            main_script.execute_avalanches(sp)

        fname = f"./../output/scale_invariance.pik"
        sp.save_avalanche_stats(fname)

        ob = sandpile.Observables(fname)
        subplot = ob.histogram(ob.radius, density=1)


""" EXECUTION """
if __name__ = "__main__":
    main()
