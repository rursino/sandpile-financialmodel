import numpy as np
import sys
from sandpile import SandPile


def execute_avalanche():
    no_avalanche = True
    while no_avalanche:
        if np.any(a.grid >= 4):
            a.avalanche()
            no_avalanche = False
        else:
            a.drop_sand()


def print_avalanche_stats():
    print(f"Avalanche duration: {a.aval_duration}")
    print(f"Number of topples: {a.topples}")
    print(f"Avalanche area: {a.area}")
    print(f"Mass lost: {a.lost_mass}")
    print(f"Avalanche radius: {a.radius}")


if __name__ == "__main__":
    length = int(sys.argv[1])
    width = int(sys.argv[2])
    num_aval_request = int(sys.argv[3])
    a = SandPile(length, width)

    for i in range(num_aval_request):
        execute_avalanche(i)

    print_avalanche_stats()
