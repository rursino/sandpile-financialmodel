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
reload(observables);

""" INPUTS """
fname = "./../../output/archive_stats/SandPile_10_10_20000.pik"
ob = observables.Observables(fname)
observable = 'aval_duration'
ob.powerlaw_fit(observable, 1.1, True, "log", "log")

""" FUNCTIONS """
def powerlaw_fit(data, cut=False, plot=False, xscale="linear", yscale="linear"):

    x, y = np.unique(data, return_counts=1)

    x = np.log10(x)
    y = np.log10(y)

    if cut:
        cut_left = (x < cut)
        cut_right = (x >= cut)

        split_xy = ((x[cut_left], y[cut_left]), (x[cut_right], y[cut_right]))
    else:
        split_xy = [(x, y)]

    fig = plt.figure(figsize=(20,10))

    regression_stats = []
    for split_x, split_y in split_xy:

        regression = stats.linregress(split_x, split_y)

        if plot:
            b, c = regression[:2]

            plt.plot(10**split_x, 10**split_y)
            y_reg = b*split_x + c
            plt.plot(10**split_x, 10**y_reg, color='r')

            c = 10**c

            plt.xscale(xscale)
            plt.yscale(yscale)

            regression_stats.append(regression[:3])

    return regression_stats

""" EXECUTION """
scale = "log"
regression = powerlaw_fit(x, 1, 1, scale, scale)
regression
