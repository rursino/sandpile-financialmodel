import numpy as np
import sys
import matplotlib.pyplot as plt

sys.path.append("./core")
import sandpile

from importlib import reload
reload(sandpile)


""" INPUTS """
length = 10
width = 10
num_aval_request = 20000

sp = sandpile.SandPile(length, width)


""" FUNCTIONS """
def execute_avalanches(sp):
    no_avalanche = True
    while no_avalanche:
        if np.any(sp.grid >= 4):
            sp.avalanche()
            no_avalanche = False
        else:
            sp.drop_sand()

def print_avalanche_stats(sp, index):
    aval_stats = sp.view_avalanche_stats(index)

    stats = ["Duration", "Topples", "Area",
    "Lost mass", "Radius"]
    for stat in stats:
        print(f"{stat}: {aval_stats[stat]}")

def save_plots(ob):
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
    for i in range(num_aval_request):
        execute_avalanches(sp)

    # print_avalanche_stats(sp, "all")
    print_avalanche_stats(sp, -1)

    fname = f"./../output/sandpile_{length}_{width}_{num_aval_request}.pik"
    sp.save_avalanche_stats(fname)

    ob = sandpile.Observables(fname)
    save_plots(ob)


""" EXECUTION """
if __name__ == "__main__":
    main()
