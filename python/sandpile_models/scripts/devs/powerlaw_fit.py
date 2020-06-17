""" Devs to fix the powerlaw_fit graphs and adding pink noise to fit.
"""

import pickle
import sys
import matplotlib.pyplot as plt
import colorednoise
from scipy import signal

sys.path.append("./../core/")
import observables

from importlib import reload
reload(observables)

fname = "./../../output/archive_stats/SandPile_10_10_20000.pik"
ob = observables.Observables(fname)

x = ob.area
scale = "log"
regression = ob.powerlaw_fit(x, 1, scale, scale)


f, X = signal.periodogram(x)
plt.loglog(f, X); plt.ylim([1e-3, 1e4])
