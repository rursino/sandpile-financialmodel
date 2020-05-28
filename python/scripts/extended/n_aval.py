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
        self.threshold = 8

    def check_threshold(self):
        """Returns the cells to topple by detecting the cells with neighbours
        that satisfy the condition that the difference in grains is at least
        the threshold set from the initialisation of the class.
        """

        neighbours = self.neighbours()

        cells_to_topple = []
        for cell in neighbours:
            ncells = neighbours[cell]

            if difference >= self.threshold:
                cells_to_topple.append(cell)

        return cells_to_topple

    def neighbours(self):
        """Returns the difference in grains between every cell and its
        neighbouring cells.
        """

        neighbours_dict = {}

        neighbours = lambda x, y : [(xx, yy) for xx in range(x-1, x+2)
                                       for yy in range(y-1, y+2)
                                       if (-1 < x < self.width and
                                           -1 < y < self.length and
                                           (x != xx or y != yy))]

        for cell in product(*(range(n) for n in (self.length, self.width))):

            i, j = cell

            neighbour_vals = []
            for ncell in neighbours(i,j):
                ii, jj = ncell
                if (0 <= ii < self.length) and (0 <= jj < self.width):
                    val = self.grid[ii][jj]
                else:
                    val = 0

                neighbour_vals.append((ncell, self.grid[i][j] - val))

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

        i, j = cell

        for ncell in self.neighbours()[cell]:
            ii, jj = ncell[0]
            difference = ncell[1]

            if difference >= self.threshold:
                self.grid[i][j] -= 1

                if (0 <= ii < self.length) and (0 <= jj < self.width):
                    self.grid[ii][jj] -= 1

        if increment_time:
            self.time += 1

    def avalanche(self):
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

        # Topple cells until all cells have less than the threshold no.
        cells_to_topple = check_threshold()
        while cells_to_topple:
            #
            #

            cells_to_topple = check_threshold()


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

zip(neighbours[(0,0)])

sp.check_threshold()