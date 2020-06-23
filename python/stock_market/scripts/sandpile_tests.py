""" Execution of stock market sandpile.
"""


""" IMPORTS """
import numpy as np
import pandas as pd
import pickle

import matplotlib.pyplot as plt

import sys
sys.path.append("./core/")
import sandpile
import analysis

from importlib import reload
reload(sandpile)
reload(analysis)


""" INPUTS """
length = 10
width = 10
threshold = 100
duration = 500


""" FUNCTIONS """
def output_results(crashes, largest_crash):
    with open('./../output/sandpile/crash_stats.txt', 'w') as f:

        f.write("S&P 500 OUTPUT\n" + "=" * 25 + "\n" * 2)

        kwargs = [crashes, largest_crash]

        #'crashes' object
        f.write("Magnitude of every crash:\n")
        for crash in kwargs[0]:
            f.write(f"{crash:.2f}%" + "\n")
        f.write("\n")

        #'largest_crash' object
        f.write("Largest crash\n" + "-" * 15 + "\n")
        largest_crash = kwargs[1]
        f.write(f"Start of crash: {largest_crash[0][0]}\n")
        f.write(f"End of crash: {largest_crash[0][1]}\n")
        f.write(f"Drop: {largest_crash[1]:.2f}%\n")

def main():
    market = sandpile.StockMarket(length, width, threshold)

    market.run_simulation(duration)
    fname = f"./../output/sandpile/{length}_{width}_{duration}.pik"
    market.save_simulation(fname)

    market_data = pickle.load(open(fname, "rb"))

    volume_history = market_data["Volume History"]

    start_time = "2020-01-01"
    end_time = np.datetime64(start_time) + np.timedelta64(len(volume_history))
    time_range = np.arange(start_time, end_time, dtype='datetime64[D]')

    x = pd.Series(np.array(volume_history), index=time_range)

    data = analysis.CrashAnalysis(x)

    crash_size = 1 # per cent.
    data.crash_detection(crash_size)

    crashes = [
        data.crash_stats(i).lost_units
        for i, _ in enumerate(data.crash_history)
        ]
    largest_crash = (
                    data.crash_history[np.argmax(crashes)],
                    np.max(crashes)
                    )

    output_results(crashes, largest_crash)

    data

    # start_crash, end_crash = largest_crash[0]
    # sub_x = x.loc[np.datetime64(start_crash) : np.datetime64(end_crash)]
    #
    # data.view_timeseries(1)
    # plt.plot(sub_x.values)
    # plt.savefig("./../output/timeseries.png")
    #
    # np.datetime64(x.index)

""" EXECUTION """
if __name__ == "__main__":
    main()
