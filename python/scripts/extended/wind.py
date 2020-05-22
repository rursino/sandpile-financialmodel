"""Development of the wind function/s."""


""" IMPORTS """
import numpy as np
import matplotlib.pyplot as plt
from itertools import *


""" FUNCTIONS """
class SandPile():

    def __init__(self, grid):

        self.grid = grid
        self.length = grid.shape[0]
        self.width = grid.shape[1]

    def wind(self, direction, speed):
        """Moves sand grains along the grid with specified direction.

        Parameters
        ==========

        direction: str

            Direction of wind. Takes either L, R, U or D.

        speed: int

            Amount of grains moved to its neighbour grid.

        """
        # Rotate grid to suit indexing for movement of grains
        grid = self.grid

        if direction == "R":
            grid = np.rot90(grid, 3)
        elif direction == "L":
            grid = np.rot90(grid, 1)
        elif direction == "D":
            grid = np.rot90(grid, 2)


        # Remove and add grains to each cell according to wind direction
        # and speed.
        for cell in product(*(range(n) for n in (self.width, self.length))):
            i, j = cell

            if grid[i][j] >= speed:
                lost_mass = speed
            else:
                lost_mass = grid[i][j]

            grid[i][j] -= lost_mass

            if direction == "R":
                ii, jj = i, j + 1
            elif direction == "L":
                ii, jj = i, j - 1
            elif direction == "U":
                ii, jj = i - 1, j
            elif direction == "D":
                ii, jj = i + 1, j

            if ((0 <= ii < self.length) and (0 <= jj < self.width)):
                grid[ii][jj] += lost_mass

        # Rotate grid back to original axis.
        if direction == "R":
            grid = np.rot90(grid, 1)
        elif direction == "L":
            grid = np.rot90(grid, 3)
        elif direction == "D":
            grid = np.rot90(grid, 2)

        return grid


""" INPUTS """
grid = np.array([
[1,4,2,4,5],
[0,1,6,3,1],
[3,5,8,2,1],
[2,1,0,0,7],
[9,1,4,3,5]
])
grid
np.rot90(grid, 3)


""" EXECUTION """
sp = SandPile(grid)
og = sp.grid.copy()
ng = sp.wind("L", 1)
ng
ng-og
