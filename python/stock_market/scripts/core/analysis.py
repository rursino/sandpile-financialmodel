"""Analysis of data from the financial markets extension phase of the project.
"""


""" IMPORTS """
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal
import numpy as np
from collections import namedtuple


# """ INPUTS """
# df = pd.read_csv("./../../data/sp500daily.csv",
#                 index_col = "Date"
#                 )
#
# x = df.Open
# x
#
# """ EXECUTION """
# a = Analysis(x)
# a.crash_detection()
# a.crash_stats(0)


""" FUNCTIONS """
class CrashAnalysis:
    """
    """

    def __init__(self, data):
        _data = data
        self.data = _data
        self.crash_history = []

    def view_timeseries(self, peaks=False, *args, **kwargs):
        """
        """

        x = self.data

        fig = plt.figure(figsize=(20,10))
        plt.plot(x.index, x.values, *args, **kwargs)
        # plt.xticks([])

        if peaks:
            imin = signal.argrelmin(x.values.squeeze(), order=6)[0]
            imax = signal.argrelmax(x.values.squeeze(), order=6)[0]

            plt.scatter(imin, x[imin], color='b')
            plt.scatter(imax, x[imax], color='r')

    def crash_detection(self, size):
        """ Detects a crash in an index fund timeseries, which is defined by a
        drop in the stock price by a percent drop (determined by the parameter
        'size') from a local peak.
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
        """ Determines the statistics of any crash.
        x = timeseries with time index and observable, which could be units or
        price.
        Need:
        - lost amount of unit.
        - crash duration.
        - investors?
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
