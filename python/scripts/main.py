import numpy as np
import sys
import matplotlib.pyplot as plt

sys.path.append("./core")
import sandpile


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

def main():
    for i in range(num_aval_request):
        execute_avalanches(sp)

    # print_avalanche_stats(sp, "all")
    print_avalanche_stats(sp, -1)

    fname = f"./../output/sandpile_{length}_{width}_{num_aval_request}.pik"
    sp.save_avalanche_stats(fname)
    ob = sandpile.Observables(fname)

    ob.histogram(ob.radius)

    # ob.prob_dist(ob.radius)
    #
    # ob.line_plot(ob.mass_history)
    #
    # ob.visualise_grid()


""" EXECUTION """
main()
# if __name__ == "__main__":
#     main()
