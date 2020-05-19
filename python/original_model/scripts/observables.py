""" Analysis of observables and development of Observables class, as part of
the Extension BTW phase.
"""

""" IMPORTS """
import numpy as np
import sys
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.append("./core")
import sandpile

from importlib import reload
reload(sandpile)


""" INPUTS """
fname = "./../output/sandpile_10_10_20000.pik"
ob = sandpile.Observables(fname)


""" EXECUTION """
x = ob.area
y = ob.radius

def reg(x, y, k):
    fig = plt.figure(figsize=(20,10))
    x = np.array(x)
    y = np.array(y)
    regression = stats.linregress(x, y)

    slope, intercept = regression[:2]
    plt.plot(x, slope*(x) + intercept, color='r')
    plt.scatter(x, y**k)

reg(x,y,2)
