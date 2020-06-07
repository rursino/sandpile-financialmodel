""" A program set for the "end" user to simulate the onset and avalanche of a
sandpile.
"""

""" IMPORTS """
import numpy as np
import sys

sys.path.append("./core")
import sandpile


""" FUNCTIONS """
# Execute avalanche only when at least one grid has 4 or more grains of sand,
# otherwise continue to drop grains at random grid locations.

def execute_avalanche():
    no_avalanche = True
    while no_avalanche:
        if my_sandpile.check_threshold():
            my_sandpile.avalanche()
            no_avalanche = False
        else:
            my_sandpile.drop_sand()

# Print stats of latest avalanche.
def print_avalanche_stats():
    sp_stats = my_sandpile.view_avalanche_stats(-1)

    print("\n")
    print(f"Avalanche duration: {sp_stats['Duration']}")
    print(f"Number of topples: {sp_stats['Topples']}")
    print(f"Avalanche area: {sp_stats['Area']}")
    print(f"Mass lost: {sp_stats['Lost mass']}")
    print("Avalanche distance: {:.2f}".format(sp_stats['Distance']))
    print("\n")


""" EXECUTION """
if __name__ == "__main__":

    # Inputs set by user at start of program.
    length = int(input("Set the length of the sandpile: "))
    width = int(input("Set the width of the sandpile: "))

    # Initialize an instance of the sandpile class.
    my_sandpile = sandpile.SandPileEXT2(length, width)

    # Execute an avalanche from criteria set from function definition and print
    # stats.
    execute_avalanche()
    print_avalanche_stats()

    # Prompt user to execute another avalanche or exit the program.
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
