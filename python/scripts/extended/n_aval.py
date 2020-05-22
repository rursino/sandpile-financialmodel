"""Development of 8 neighbour cells toppling.
"""


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

    def neighbours(self):
        """Returns the difference in grains between every cell and its
        neighbouring cells.
        """

        neighbours_dict = {}

        neighbours = lambda x, y : [(xx, yy) for xx in range(x-1, x+2)
                                       for yy in range(y-1, y+2)
                                       if (-1 < x < self.width and
                                           -1 < y < self.length and
                                           (x != xx or y != yy) and
                                           (0 <= xx < self.width) and
                                           (0 <= yy < self.length))]

        for cell in product(*(range(n) for n in (self.length, self.width))):

            i, j = cell

            neighbour_vals = []
            for ncell in neighbours(i,j):
                ii, jj = ncell
                neighbour_vals.append(self.grid[ii][jj] - self.grid[i][j])

            neighbours_dict[cell] = neighbour_vals

        return neighbours_dict

    def topple(self, cell, increment_time=False):
        """Topple the specified cell.
        Parameters
        ==========

        cell: tuple-like

            The address of the cell to topple.

        increment_time: bool

            Whether to increment one time step or not. Defaults to False.

        """

        raise NotImplementedError()
        # change to -8 and add 1 to the 8 surrounding cells

        i, j = cell

        self.grid[i][j] -= 4

        if i != 0:
            self.grid[i-1][j] += 1
        if i != self.length - 1:
            self.grid[i+1][j] += 1
        if j != 0:
            self.grid[i][j-1] += 1
        if j != self.width - 1:
            self.grid[i][j+1] += 1

        if increment_time:
            self.time += 1

    def avalanche(self):# Other params: start?
        """Run the avalanche causing all cells to topple and store the stats of
        the avalanche in the appropriate variables.
        For extended sandpile, avalanches are run when the difference between
        any cell and any of its neighbours reaches a threshold.

        Parameters
        ==========

        name: string

            Given name for the avalanche.

        """

        # Initialize avalanche statistics.
        num_of_topples = 0
        toppled_cells = []
        start_mass = self.mass()
        start_time = self.time

        # Record first toppled cell for calculation of distance.
        first_toppled_cell = []

        # Gather difference of grains between cells and their neighbours.
        neighbours = self.neighbours()

        # Check for differences between neighbouring cells over the threshold.
        for key in neighbours:
            val = np.array(neighbours[key])
            np.any(val <= -self.threshold)

        # Topple cells until all cells have less than the threshold no.
        while np.any(self.grid >= self.threshold):
            # Extact cells to topple.
            topple_locations = np.where(self.grid >= self.threshold)
            all_i = topple_locations[0]
            all_j = topple_locations[1]

            if not first_toppled_cell:
                first_toppled_cell.append(all_i[0])
                first_toppled_cell.append(all_j[0])

            # Topple each cell and update avalanche statistics.
            for topple_number in range(len(all_i)):

                cell = (all_i[topple_number], all_j[topple_number])

                self.topple(cell)

                num_of_topples += 1
                toppled_cells.append(cell)

            self.time += 1

        # Record observables into the avalanche_stats attributes
        unique_toppled_cells = np.unique(toppled_cells, axis=0)

        # Calculate 'area' = number of unique toppled cells.
        area = len(unique_toppled_cells)

        # Calculate distance.
        difference_i = unique_toppled_cells.T[0] - first_toppled_cell[0]
        difference_j = unique_toppled_cells.T[1] - first_toppled_cell[1]
        distance = abs(difference_i) + abs(difference_j)
        max_distance = max(distance)

        # Record all stats into avalanche_stats.
        self.aval_duration.append(self.time - start_time)
        self.num_of_avalanches += 1
        self.topples.append(num_of_topples)
        self.area.append(area)
        self.lost_mass.append(start_mass - self.mass())
        self.distance.append(max_distance)


""" INPUTS """
grid = np.array([
[1,4,2,4,5],
[0,1,6,3,1],
[3,5,8,2,1],
[2,1,0,0,7],
[9,1,4,3,5]
])


""" EXECUTION """
sp = SandPile(grid)
neighbours = sp.neighbours()
ex = np.array(neighbours[(0,0)])
ex
np.any(ex <= 4)
for key,val in neighbours:
    print(key,val)
