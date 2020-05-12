import numpy as np
import sys

sys.path.append("./core")
from sandpile import SandPile

def execute_avalanche():
    no_avalanche = True
    while no_avalanche:
        if np.any(a.grid >= 4):
            a.avalanche()
            no_avalanche = False
        else:
            a.drop_sand()

def print_avalanche_stats(name, dict_stat):
    print("\n")
    print(f"Name of avalanche: {name}")
    print(f"Time at end of avalanche: {dict_stat[0]}")
    print(f"Number of topples: {dict_stat[1]}")
    print(f"Avalanche area: {dict_stat[2]}")
    print(f"Mass lost: {dict_stat[3]}")
    print("Avalanche radius: {:.2f}".format(dict_stat[4]))
    print("\n")


if __name__ == "__main__":
    length = int(sys.argv[1])
    width = int(sys.argv[2])
    sandpile = SandPile(length, width)

    execute_avalanche()

    ask_again = True
    while ask_again:
        x = input("Go again? Answer YES or NO: ")
        if x == "YES":
            execute_avalanche()
        elif x == "NO":
            ask_again = False
        else:
            print("Invalid answer. I will ask again.")
