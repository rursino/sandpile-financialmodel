import numpy as np
import sys

sys.path.append("./core")
import sandpile

def execute_avalanche():
    no_avalanche = True
    while no_avalanche:
        if np.any(my_sandpile.grid >= 4):
            my_sandpile.avalanche()
            no_avalanche = False
        else:
            my_sandpile.drop_sand()

def print_avalanche_stats():
    sp_stats = my_sandpile.view_avalanche_stats(-1)

    print("\n")
    print(f"Avalanche duration: {sp_stats['Duration']}")
    print(f"Number of topples: {sp_stats['Topples']}")
    print(f"Avalanche area: {sp_stats['Area']}")
    print(f"Mass lost: {sp_stats['Lost mass']}")
    print("Avalanche radius: {:.2f}".format(sp_stats['Radius']))
    print("\n")


if __name__ == "__main__":
    length = int(sys.argv[1])
    width = int(sys.argv[2])
    my_sandpile = sandpile.SandPile(length, width)

    execute_avalanche()
    print_avalanche_stats()

    ask_again = True
    while ask_again:
        x = input("Go again? Answer YES or NO: ")
        if x == "YES":
            execute_avalanche()
            print_avalanche_stats()
        elif x == "NO":
            ask_again = False
        else:
            print("Invalid answer. I will ask again.")
