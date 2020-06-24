""" Main program: Simulates a sequence of avalanches and saves statistics
to observables.

Run in terminal as follows:
python tests.py length width num_aval_request setting sandpile_class
"""

""" IMPORTS """
import numpy as np
import sys
import os
from time import sleep
import matplotlib.pyplot as plt
import pickle
from collections import namedtuple
from itertools import product

sys.path.append("./../core")
import sandpile
import observables


""" INPUTS """

Settings = namedtuple('Settings',
                        [
                        'directory',
                        'cell',
                        'n'
                        ]
                        )

length = int(sys.argv[1])
width = int(sys.argv[2])
num_aval_request = int(sys.argv[3])

# BASIC setting.
basic = Settings("basic/", None, 1)

# CENTRE_OF_GRID setting.
i = int(((length + 1) / 2) - 1)
j = int(((width + 1) / 2) - 1)
centre_of_grid = Settings("centre_of_grid/", [(i, j)], 1)

# TOP LEFT QUARTER
tlq_cells = list(product(range(i), range(j)))
top_left_qtr = Settings("top_left_qtr/", tlq_cells, 1)

# DROP 4 GRAINS
four_grains = Settings("four_grains/", None, 4)

# DROP RANDOM AMOUNT OF GRAINS
random_grains = Settings("random_grains/", None, range(6))

# SETTING APPLIED HERE
setting = vars()[sys.argv[4]]


""" SETUP """

cell = setting.cell
n = setting.n

# Initialize sandpile.
sandpile_class = sys.argv[5]
sp = getattr(sandpile, sandpile_class)(length, width)

# Directories
DIRECTORY = f"./../../output/tests/{setting.directory}{sandpile_class}/"
if not os.path.isdir(DIRECTORY):
    os.mkdir(DIRECTORY)

DIRECTORY += f"{length}_{width}_{num_aval_request}/"
if not os.path.isdir(DIRECTORY):
    os.mkdir(DIRECTORY)

""" FUNCTIONS """
def progress_bar(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)

        index = args[-1] + 1
        total = num_aval_request
        ratio = index/total

        sys.stdout.write('\r')
        sys.stdout.write("[%-20s] %d%% %i/%i" % ('='*int(20*ratio),
        (100*ratio),
        index,
        total))
        sys.stdout.flush()

    return wrapper

# Execute an avalanche at time of request.
@progress_bar
def execute_avalanches(sp, index, n=1, cell=None, increment_time=False):
    no_avalanche = True
    while no_avalanche:
        if sp.check_threshold():
            sp.avalanche(increment_time)
            no_avalanche = False
        else:
            sp.drop_sand(n=n, cell=cell)

# Print stats for any avalanche.
def print_avalanche_stats(sp, index):
    aval_stats = sp.view_avalanche_stats(index)

    stats = ["Duration", "Topples", "Area",
    "Lost mass", "Distance"]
    for stat in stats:
        print(f"{stat}: {aval_stats[stat]}")

# Run through and save the plots of the powerlaw fits.
def powerlaw_plots(ob, dir):

    names = ("aval_duration", "topples", "area", "lost_mass", "distance")

    for observable in names:

        ob.powerlaw_fit(observable, False, 1, "log", "log")
        plt.show()

        data = getattr(ob, observable)
        x, y = np.unique(data, return_counts=1)
        print(np.log10(x), np.log(y))
        cut = input("Where should the data be split (cut)?  ")

        plt.close()
        cut_valid = True
        while cut_valid:
            if cut == "end":
                exit()
            try:
                cut = float(cut)
                ob.powerlaw_fit(observable, cut, 1, "log", "log")
            except:
                cut = input("Invalid number. Try again: ")
            else:
                cut_valid = False

        plt.savefig(f"{dir}{observable}_powerlawfit.png")
        plt.close()

# Save plots of histograms, line plots and heatmap of grid.
def save_plots(ob, dir):

    # names = ("aval_duration", "topples", "area", "lost_mass", "distance")
    names = ("aval_duration")

    for observable in names:

        ob.histogram(observable, density=1)
        plt.savefig(f"{dir}{observable}_histogram.png")
        plt.close()

        try:
            ob.distpdf(observable, 1)
        except:
            print(f"WARNING: {observable} distpdf could not be produced.")

        plt.savefig(f"{dir}{observable}_pdf.png")
        plt.close()

    ob.line_plot('mass_history')
    plt.savefig(f"{dir}mass_history.png")
    plt.close()

    ob.visualise_grid()
    plt.savefig(f"{dir}heatmap_grid.png")
    plt.close()


def main():

    print("\n"+"="*30)
    print("MAIN.PY: OUTPUT FOR EXTENDED SANDPILE AVALANCHE")
    print("="*30+"\n\n")
    print(f"\nDimensions: {length} {width}")
    sleep(1)

    # Execute avalanche a set number of times (set from input).
    print("-"*30+"\n")
    print(f"Executing {num_aval_request} avalanches...\n")

    for index in range(num_aval_request):
        execute_avalanches(
                        sp,
                        index,
                        n=n,
                        cell=cell,
                        increment_time=1
                        )

    sleep(0.5)
    print("\n\nDone!\n")
    print("-"*30+"\n\n")
    sleep(1)

    # Save sandpile stats to enable initialization of instance of
    # observables class.
    fname = f"{DIRECTORY}aval_stats.pik"
    sp.save_avalanche_stats(fname)
    print(f"aval_stats dictionary dumped to {fname}!\n")

    # Initialize observables class with sandpile stats above and save plots.
    ob = observables.Observables(fname)

    # Save plots of observables.
    save_plots(ob, DIRECTORY)

    print(f"Figures saved to directory {fname}")
    print("\n"+"-"*30+"\n")

    print("Program finished!\n")
    print("="*30)
    sleep(2)

def powerlaw():
    fname = f"{DIRECTORY}aval_stats.pik"
    ob = observables.Observables(fname)
    powerlaw_plots(ob, DIRECTORY)

""" EXECUTION """
if __name__ == "__main__":
    # main()
    powerlaw()
