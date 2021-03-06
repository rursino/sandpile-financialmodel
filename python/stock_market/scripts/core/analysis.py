"""Analysis of data from the financial markets extension phase of the project.
"""


""" IMPORTS """
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal
import numpy as np
from collections import namedtuple


""" FUNCTIONS """
class CrashAnalysis:
    """
    """

    def __init__(self, data):
        _data = data
        self.data = _data
        self.crash_history = []

    def view_timeseries(self, peaks=False):
        """ Plots the timeseries with the option to plot the local peaks and
        troughs.

        Parameters
        ==========

        peaks: bool

            Plot the peaks and troughs of the timeseries.
            Defaults to False.

        """

        x = self.data

        fig, ax = plt.subplots(figsize=(20,10))
        ax.plot(x)
        ax.set_xticks(ax.get_xticks()[::int(5040/len(x))])

        if peaks:
            imin = signal.argrelmin(x.values.squeeze(), order=6)[0]
            imax = signal.argrelmax(x.values.squeeze(), order=6)[0]

            ax.scatter(x[imin].index, x[imin].values, color='b')
            ax.scatter(x[imax].index, x[imax].values, color='r')

    def crash_detection(self, size):
        """ Detects a crash in an index fund timeseries, which is defined by a
        drop in the stock price by a percent drop (determined by the parameter
        'size') from a local peak.

        Parameters
        ==========

        size: int, float

            The minimum size of a drop from a local peak that classifies as a
            crash.

        """

        drop_ratio = (100 - size) / 100

        x = self.data

        order = int(len(x)/42)
        imin = signal.argrelmin(x.values.squeeze(), order = order)[0]
        imax = signal.argrelmax(x.values.squeeze(), order = order)[0]

        for maxi, max_index in enumerate(imax):
            try:
                min_index = imin[(max_index < imin) &
                                    (imin < imax[maxi + 1])][-1]
            except IndexError:
                continue

            sub_x = x[max_index : min_index + 1]

            threshold = drop_ratio * x[max_index]
            if np.any(sub_x < threshold):
                start = sub_x.index[0]
                end = sub_x.index[-1]
                self.crash_history.append((start, end))

    def crash_stats(self, crash_index):
        """ Determines the statistics of any crash from the crash_history class
        attribute.

        Parameters
        ==========

        crash_index: int

            Index of the list from the class_history attribute.
        """

        start, end = self.crash_history[crash_index]
        x = self.data.loc[start:end]

        index = x.index
        vals = x.values.squeeze()

        peak_val = np.max(vals)
        lowest_val = np.min(vals)

        percent_size = (peak_val - lowest_val) / peak_val
        duration = np.timedelta64(
                    np.datetime64(index[-1]) - np.datetime64(index[0]),
                    'D'
                    ).astype(int)

        crashStats = namedtuple('crashStats',
                                ['time', 'duration', 'lost_units'])

        return crashStats((start, end),
                            duration,
                            percent_size * 100)
