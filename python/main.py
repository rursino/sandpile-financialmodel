import numpy as np
import sys
from sandpile import SandPile


def execute_avalanche(name):
    num_of_avalanches = 0
    no_avalanche = True
    while no_avalanche:
        if np.any(a.grid >= 4):
            a.avalanche(name)
            no_avalanche = False
            num_of_avalanches += 1
        else:
            a.drop_sand()

    return num_of_avalanches


def print_avalanche_stats(dict_stat):
    print("\n")
    print(f"Time at end of avalanche: {dict_stat[0]}")
    print(f"Number of topples: {dict_stat[1]}")
    print(f"Avalanche area: {dict_stat[2]}")
    print(f"Mass lost: {dict_stat[3]}")
    print("Avalanche radius: {:.2f}".format(dict_stat[4]))
    print("\n")


if __name__ == "__main__":
    length = int(sys.argv[1])
    width = int(sys.argv[2])
    num_aval_request = int(sys.argv[3])
    a = SandPile(length, width)

    num_of_avalanches = 0
    for i in range(num_aval_request):
        num_of_avalanches += execute_avalanche(i)

    print(num_of_avalanches)
    print_avalanche_stats(a.avalanche_stats[1])
