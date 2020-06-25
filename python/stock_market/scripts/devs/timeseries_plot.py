""" Developments for the analysis timeseries plot.
"""

""" IMPORTS """
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal
import numpy as np
import pickle


""" INPUTS """
df = pd.read_csv("./../../data/sp500daily.csv",
                index_col = "Date"
                )

x = df.Open

# sp = pickle.load(open("./../../output/sandpile/10_10_5000.pik", "rb"))
# x = sp["Volume History"]
#
# start_time = "2020-01-01"
# end_time = np.datetime64(start_time) + np.timedelta64(len(x))
# time_range = np.arange(start_time, end_time, dtype='datetime64[D]')
#
# x = pd.Series(np.array(x), index=time_range)

""" FUNCTIONS """
def view_timeseries(x, peaks=False):
    """ Plots the timeseries with the option to plot the local peaks and
    troughs.

    Parameters
    ==========

    peaks: bool

        Plot the peaks and troughs of the timeseries.
        Defaults to False.

    """

    fig, ax = plt.subplots(figsize=(20,10))
    ax.plot(x)
    ax.set_xticks(ax.get_xticks()[::int(5040/len(x))])

    if peaks:
        imin = signal.argrelmin(x.values.squeeze(), order=6)[0]
        imax = signal.argrelmax(x.values.squeeze(), order=6)[0]

        ax.scatter(x[imin].index, x[imin].values, color='b')
        ax.scatter(x[imax].index, x[imax].values, color='r')


""" EXECUTION """
view_timeseries(x, True)
