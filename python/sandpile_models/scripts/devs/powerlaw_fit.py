""" Devs to fix the powerlaw_fit graphs and adding pink noise to fit.
"""

""" IMPORTS """

import pickle
import sys
import matplotlib.pyplot as plt
import colorednoise
from scipy import signal
import numpy as np
from scipy import stats

sys.path.append("./../core/")
import observables

from importlib import reload
reload(observables)

""" INPUTS """

fname = "./../../output/archive_stats/SandPile_10_10_20000.pik"
ob = observables.Observables(fname)
x = ob.area


""" FUNCTIONS """
def powerlaw_fit(data, plot=False, xscale="linear", yscale="linear"):

    x, y = np.unique(data, return_counts=1)

    x = np.log10(x)
    y = np.log10(y)

    regression = stats.linregress(x, y)

    if plot:
        b, c = regression[:2]

        fig = plt.figure(figsize=(20,10))
        plt.plot(10**x, 10**y)
        y_reg = b*x + c
        plt.plot(10**x, 10**y_reg, color='r')

        c = 10**c

        plt.xscale(xscale)
        plt.yscale(yscale)

    return regression[:3]


""" EXECUTION """
scale = "log"
regression = powerlaw_fit(x, 1, scale, scale)
