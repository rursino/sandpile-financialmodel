""" Main program: Simulates a sequence of avalanches and saves statistics
to observables.
"""

""" IMPORTS """
import numpy as np
import sys
import matplotlib.pyplot as plt

sys.path.append("./core")
import sandpile

from importlib import reload
reload(sandpile)


""" INPUTS """
# Dimensions for grid.
length = 10
width = 10

# Requested number of avalanches (by user).
num_aval_request = 20000

# Initialize sandpile.
sp = sandpile.SandPile(length, width)


""" FUNCTIONS """
# Execute an avalanche at time of request.
def execute_avalanches(sp):
    no_avalanche = True
    while no_avalanche:
        if np.any(sp.grid >= 4):
            sp.avalanche()
            no_avalanche = False
        else:
            sp.drop_sand()

# Print stats for any avalanche.
def print_avalanche_stats(sp, index):
    aval_stats = sp.view_avalanche_stats(index)

    stats = ["Duration", "Topples", "Area",
    "Lost mass", "Radius"]
    for stat in stats:
        print(f"{stat}: {aval_stats[stat]}")

# Save plots of histograms, line plots and heatmap of grid.
def save_plots(ob):
    # Directory to save plots.
    dir = "./../output/plots/"

    ob.histogram(ob.aval_duration, density=1)
    plt.savefig(f"{dir}aval_duration_pdf.png")
    ob.histogram(ob.topples, density=1)
    plt.savefig(f"{dir}topples_pdf.png")
    ob.histogram(ob.area, density=1)
    plt.savefig(f"{dir}area_pdf.png")
    ob.histogram(ob.lost_mass, density=1)
    plt.savefig(f"{dir}lost_mass_pdf.png")
    ob.histogram(ob.radius, density=1)
    plt.savefig(f"{dir}radius_pdf.png")

    ob.line_plot(ob.mass_history)
    plt.savefig(f"{dir}mass_history.png")

    ob.visualise_grid()
    plt.savefig(f"{dir}heatmap_grid.png")

    x = ob.radius
    y = ob.aval_duration
    k = 3
    ob.regression(x=x, y=y, k=k, plot=1)
    plt.savefig(f"{dir}reg_avalduration_{k}.png")


def main():
    # Execute avalanche a set number of times (set from input).
    for i in range(num_aval_request):
        execute_avalanches(sp)

    # Print stats of last avalanche.
    print_avalanche_stats(sp, -1)

    # Save sandpile stats to enable initialization of instance of
    # observables class.
    fname = f"./../output/sandpile_{length}_{width}_{num_aval_request}.pik"
    sp.save_avalanche_stats(fname)

    # Initialize observables class with sandpile stats above and save plots.
    ob = sandpile.Observables(fname)
    save_plots(ob)


""" EXECUTION """
if __name__ == "__main__":
    main()
