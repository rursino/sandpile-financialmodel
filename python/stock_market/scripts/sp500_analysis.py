"""Analysis and output of S&P 500 data on the analysis.CrashAnalysis class.
"""

""" IMPORTS """
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle

import sys
sys.path.append("./core/")
import analysis


""" INPUTS """
df = pd.read_csv("./../data/sp500daily.csv",
                index_col = "Date"
                )

x = df.Open


""" FUNCTIONS """
def output_results(crashes, largest_crash):
    with open('./../output/sp500/crash_stats.txt', 'w') as f:

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
    sp500 = analysis.CrashAnalysis(x)

    crash_size = 20 # per cent.
    sp500.crash_detection(crash_size)

    crashes = [
        sp500.crash_stats(0).lost_units
        for i, _ in enumerate(sp500.crash_history)
    ]

    largest_crash = (
                    sp500.crash_history[np.argmax(crashes)],
                    np.max(crashes)
                        )

    output_results(crashes=crashes, largest_crash=largest_crash)


""" EXECUTION """
if __name__ == "__main__":
    main()
