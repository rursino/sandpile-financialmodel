""" Main program: Simulates a sequence of avalanches and saves statistics
to observables.
"""

""" IMPORTS """
import numpy as np
import sys
import os
from time import sleep
import matplotlib.pyplot as plt
import pickle

sys.path.append("./../core")
import sandpile
import observables

# from importlib import reload
# reload(sandpile)
# reload(observables)


""" INPUTS """
# Dimensions for grid.
length = int(sys.argv[1])
width = int(sys.argv[2])

# Requested number of avalanches (by user).
num_aval_request = 2000

# Initialize sandpile.
sandpile_class = sandpile.SandPile
sp = sandpile_class(length, width)

# Directories
DIRECTORY = f"./../../output/"
MODEL_DIR = f"{sandpile_class.__name__}/"

dir = DIRECTORY + MODEL_DIR
if not os.path.isdir(dir):
    os.mkdir(dir)

dir += f"{length}_{width}_{num_aval_request}/"
if not os.path.isdir(dir):
    os.mkdir(dir)


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
            sp.drop_sand(cell=cell)

# Print stats for any avalanche.
def print_avalanche_stats(sp, index):
    aval_stats = sp.view_avalanche_stats(index)

    stats = ["Duration", "Topples", "Area",
    "Lost mass", "Distance"]
    for stat in stats:
        print(f"{stat}: {aval_stats[stat]}")

# Save plots of histograms, line plots and heatmap of grid.
def save_plots(ob, dir):

    names = {
    "aval_duration": ob.aval_duration,
    "topples": ob.topples,
    "area": ob.area,
    "lost_mass": ob.lost_mass,
    "distance": ob.distance
    }

    for name in names:
        observable = names[name]

        ob.histogram(observable, density=1)
        plt.savefig(f"{dir}{name}_histogram.png")
        plt.clf()

        try:
            ob.distpdf(observable, 1)
        except:
            print(f"WARNING: {name} distpdf could not be produced.")
            pass
        plt.savefig(f"{dir}{name}_pdf.png")
        plt.clf()

        ob.powerlaw_fit(observable, 1, "log", "log")
        plt.savefig(f"{dir}{name}_powerlawfit.png")
        plt.clf()

    ob.line_plot(ob.mass_history)
    plt.savefig(f"{dir}mass_history.png")
    plt.clf()

    ob.visualise_grid()
    plt.savefig(f"{dir}heatmap_grid.png")
    plt.clf()

    # x = ob.distance
    # y = ob.aval_duration
    # types = "linear", "powerlaw"
    # scales = "linear", "log"
    # remove_zeroes = 0, 1
    # for (type, scale, rz) in zip(types, scales, remove_zeroes):
    #     regression = ob.regression(x, y, type, rz, 1, scale, scale)
    #     plt.savefig(f"{dir}reg_avalduration_{type}.png")
    #     plt.clf()
    #     pickle.dump(regression, open(f"{dir}reg_avalduration_{type}.pik", "wb"))

def begin_program():
    print("\n"+"="*30)
    print("MAIN.PY: OUTPUT FOR EXTENDED SANDPILE AVALANCHE")
    print("="*30+"\n\n")
    print(f"\nDimensions: {length} {width}")
    sleep(1)

def centre_of_grid():
    i = (((length + 1) / 2) - 1)
    j = (((width + 1) / 2) - 1)
    return int(i), int(j)

def main():

    begin_program()

    # Execute avalanche a set number of times (set from input).
    print("-"*30+"\n")
    print(f"Executing {num_aval_request} avalanches...\n")

    # Determine which cell to drop sand on.
    cell = None

    # Determine how many grains of sand to drop in at one time.
    n = 1

    # Determine how to increment time dueing avalanche.
    increment_time = True

    for index in range(num_aval_request):
        execute_avalanches(
                        sp,
                        index,
                        n=n,
                        cell=cell,
                        increment_time=increment_time
                        )

    sleep(0.5)
    print("\n\nDone!\n")
    print("-"*30+"\n\n")
    sleep(1)

    # Save sandpile stats to enable initialization of instance of
    # observables class.
    fname = f"{dir}aval_stats.pik"
    sp.save_avalanche_stats(fname)
    print(f"aval_stats dictionary dumped to {fname}!\n")

    # Initialize observables class with sandpile stats above and save plots.
    ob = observables.Observables(fname)

    # Save plots of observables.
    save_plots(ob, dir)

    print(f"Figures saved to directory {fname}")
    print("\n"+"-"*30+"\n")

    print("Program finished!\n")
    print("="*30)
    sleep(2)


""" EXECUTION """
if __name__ == "__main__":
    main()
