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

sys.path.append("./core")
import sandpile as sandpile
import observables

from importlib import reload
reload(sandpile)


""" INPUTS """
# Dimensions for grid.
length = 15
width = 15

# Requested number of avalanches (by user).
num_aval_request = 5000

# Initialize sandpile.
sp = sandpile.SandPile(length, width)


""" FUNCTIONS """
def progress_bar(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)

        i = args[-1] + 1
        total = num_aval_request
        ratio = i/total

        sys.stdout.write('\r')
        sys.stdout.write("[%-20s] %d%% %i/%i" % ('='*int(20*ratio),
        (100*ratio),
        i,
        total))
        sys.stdout.flush()

    return wrapper

# Execute an avalanche at time of request.
@progress_bar
def execute_avalanches(sp, i):
    no_avalanche = True
    while no_avalanche:
        if sp.check_threshold():
            sp.avalanche()
            no_avalanche = False
        else:
            sp.drop_sand()

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

    x = ob.distance
    y = ob.aval_duration
    type = "linear"
    regression = ob.regression(x, y, type, 0, 1, "log", "log")
    plt.savefig(f"{dir}reg_avalduration_{type}.png")
    plt.clf()
    pickle.dump(regression, open(f"{dir}reg_avalduration_{type}", "wb"))


def main():

    print("\n"+"="*30)
    print("MAIN.PY: OUTPUT FOR EXTENDED SANDPILE AVALANCHE")
    print("="*30+"\n\n")
    sleep(1)

    # Execute avalanche a set number of times (set from input).
    print("-"*30+"\n")
    print(f"Executing {num_aval_request} avalanches...\n")
    for i in range(num_aval_request):
        execute_avalanches(sp, i)

    sleep(0.5)
    print("\n\nDone!\n")
    print("-"*30+"\n\n")
    sleep(1)

    # Print stats of last avalanche.
    print("Statistics to last avalanche shown below:\n")
    print_avalanche_stats(sp, -1)
    print("\n"+"-"*30+"\n")

    # Save sandpile stats to enable initialization of instance of
    # observables class.
    for sec in range(5):
        seconds_left = 5 - sec
        if seconds_left == 1:
            second_str = "second"
        else:
            second_str = "seconds"
        sys.stdout.write(f"\rSaving plots in {seconds_left} {second_str}...")
        sys.stdout.flush()
        sleep(1)
    print("\n")

    fname = f"./../output/sandpile_{length}_{width}_{num_aval_request}.pik"
    sp.save_avalanche_stats(fname)
    print(f"aval_stats dictionary dumped to {fname}!\n")

    # Initialize observables class with sandpile stats above and save plots.
    ob = sandpile.Observables(fname)

    # Directory to save plots.
    dir = f"./../output/plots/{length}_{width}_{num_aval_request}/"
    if os.path.isdir(dir):
        save_plots(ob, dir)
    else:
        os.mkdir(dir)
        save_plots(ob, dir)

    print(f"Figures saved to directory {dir}")
    print("\n"+"-"*30+"\n")

    print("Program finished!\n")
    print("="*30)
    sleep(2)


""" EXECUTION """
if __name__ == "__main__":
    main()

fname = f"./../output/sandpile_{length}_{width}_{num_aval_request}.pik"
ob = observables.Observables(fname)
ob.histogram(ob.area, density=1)
ob.line_plot(ob.mass_history)
ob.visualise_grid()
ob.distpdf(ob.area)
ob.powerlaw_fit(ob.area, 1, "log", "log")
