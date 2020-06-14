""" Development of pink noise to add to sandpile statistical models.
"""

import colorednoise
import matplotlib.pyplot as plt
from scipy import signal

x = colorednoise.powerlaw_psd_gaussian(1, 100000); f,y = signal.periodogram(x); plt.loglog(f,y)


x = colorednoise.powerlaw_psd_gaussian(1, 20); plt.plot(x)
