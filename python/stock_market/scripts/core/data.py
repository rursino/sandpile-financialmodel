"""Analysis of data from the financial markets extension phase of the project.
"""


""" IMPORTS """
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal

""" S&P 500 """
df = pd.read_csv("./../../data/sp500daily.csv",
                index_col = "Date"
                )
df
x = df.index
y1 = df.Open
y2 = df.Volume

ipeaks = signal.find_peaks(y1)[0]

fig = plt.figure(figsize=(20,10))
ax = fig.add_subplot(111)
ax.plot(y1)
ax.set_ylabel('Day Open Price')
plt.scatter(ipeaks, y1[ipeaks], color='r')

def detect_a_crash(x):
    """ Detects a crash in an index fund timeseries, which is defined by a drop
    in the stock price by 20% from a local peak.
    """

    ipeaks = signal.find_peaks(x)

    for peak in ipeak
