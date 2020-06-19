"""Analysis of data from the financial markets extension phase of the project.
"""


""" IMPORTS """
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal
import numpy as np

""" S&P 500 """
df = pd.read_csv("./../../data/sp500daily.csv",
                index_col = "Date"
                )

x = df.index
y1 = df.Open
y2 = df.Volume

imin = signal.argrelmin(y1.values, order=6)[0]
imax = signal.argrelmax(y1.values, order=6)[0]

fig = plt.figure(figsize=(20,10))
ax = fig.add_subplot(111)
ax.plot(y1)
ax.set_ylabel('Day Open Price')
plt.scatter(imin, y1[imin], color='r')
plt.scatter(imax, y1[imax], color='b')

def crash_detection(x):
    """ Detects a crash in an index fund timeseries, which is defined by a drop
    in the stock price by 20% from a local peak.
    """

    order = int(len(x)/42)
    imin = signal.argrelmin(x.values, order = order)[0]
    imax = signal.argrelmax(x.values, order = order)[0]

    crash = []
    for maxi, max_index in enumerate(imax):
        try:
            min_index = imin[(max_index < imin) & (imin < imax[maxi + 1])][-1]
        except IndexError:
            pass

        sub_x = x[max_index : min_index + 1]

        threshold = 0.8 * x[max_index]
        if np.any(sub_x < threshold):
            crash.append(sub_x)

    return crash

crash_detection(y1)

imin
imax
