import numpy as np
import sys
from sandpile import SandPile

def execute_avalanche(name):
    no_avalanche = True
    while no_avalanche:
        if np.any(a.grid >= 4):
            a.avalanche(name)
            print(a.avalanche_stats)
            no_avalanche = False
        else:
            a.drop_sand()


if __name__ == "__main__":
    length = int(sys.argv[1])
    width = int(sys.argv[2])
    a = SandPile(length, width)

    execute_avalanche("The First Avalanche")

    ask_again = True
    while ask_again:
        x = input("Go again? Answer YES or NO: ")
        if x == "YES":
            name = input("Name of avalanche? ")
            execute_avalanche(name)
        elif x == "NO":
            ask_again = False
        else:
            print("Invalid answer. I will ask again.")
