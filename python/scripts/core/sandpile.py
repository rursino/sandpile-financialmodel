""" THE BASIC SANDPILE MODEL:
This program establishes the set of functions to form the basic form of
the sandpile model with a set of subroutines for the NxN sandpile grid.

Details:
- Toppling simply occurs when a cell has 4 or more grains of sand at any time.
- Toppling consists of a loss of 4 grains at the toppled cell and adding 1
grain to each neighbouring cell to its left, right, up and down.

"""


""" IMPORTS """

from itertools import *
import numpy as np
import matplotlib.pyplot as plt
import pickle


""" FUNCTIONS """

class SandPile:

    def __init__(self, length, width, threshold=4):
        """Initialize a sandpile with the specified length and width."""
        self.length = length
        self.width = width
        self.threshold = threshold

        self.grid = np.zeros((length, width), dtype=int)

        # Track the overall mass of the sand pile overtime. The array will
        # store the masses at each time step.
        # Use len(self.mass_history) to track the number of time steps.
        self.mass_history = []

        # Track the time of the course of the sandpile.
        self.time = 0

        # Record the observables of each avalanche.
        self.aval_duration = []
        self.num_of_avalanches = 0
        self.topples = []
        self.area = []
        self.lost_mass = []
        self.distance = []

    def plot_mass(self, start_time=None, end_time=None):
        """ Plots the mass of the grid over its lifetime.

        Parameters
        ==========

        start_time: int

            The first time point to show in plot. Defaults to None.

        end_time: int

            The last time point to show in plot. Defaults to None.

        """

        if end_time:
            end_time += 1

        time = np.arange(self.time)[start_time:end_time]
        mass = np.array(self.mass_history)[start_time:end_time]

        plt.plot(time, mass)

    def drop_sand(self, n=1, cell=None):
        """Add `n` grains of sand to the grid.  Each grains of sand is added to
        a random cell (or site).

        This function also increments the time by 1 and update the internal
        `mass_history`.  Depending on how you want to code things, you may wish
        to also run the avalanche (alternatively, the avalanching might be
        executed elsewhere).

        Parameters
        ==========

        n: int

          The number of grains of sand of drop at this time step.  If left
          unspecified, defaults to 1.

        cell: tuple (i,j)

          The cell on which the grain(s) of sand should be dropped.  If `None`,
          a random cell is used.

        """

        if cell:
            i,j = cell
        else:
            i = np.random.randint(self.length)
            j = np.random.randint(self.width)

        self.grid[i][j] += n

        # Increment time by 1 and update internal mass_history.
        self.time += 1
        self.mass_history.append(np.sum(self.grid)) # Can we put mass func here?



    def mass(self):
        """Return the mass of the grid."""

        return np.sum(self.grid)

    def average_mass(self):
        """Return the average mass (or height) of the grid."""

        return self.mass()

        return (np.sum(self.grid))/(self.length * self.width)

    def check_threshold(self):
        """Returns the cells to topple because they contain a number of grains
        that is at or over the threshold set from the initialisation of the
        class.
        """

        return list(zip(*np.where(self.grid >= self.threshold)))

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

        # Topple cells until all cells have less than the threshold no.
        cells_to_topple = self.check_threshold()
        while cells_to_topple:
            # Topple each cell and update avalanche statistics.
            for cell in cells_to_topple:
                self.topple(cell)

                if not first_toppled_cell:
                    first_toppled_cell.append(cell[0])
                    first_toppled_cell.append(cell[1])

                toppled_cells.append(cell)
                num_of_topples += 1

            cells_to_topple = self.check_threshold()

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

    def view_avalanche_stats(self, aval_index):
        """View the stats of any avalanche or all avalanches.

        Parameters
        ==========

        aval_index: int or string

            Index of lists to get any avalanche, or 'all' gives entirety of
            all lists.

        """

        aval_stats = {}

        if aval_index == "all":
            aval_stats["Duration"] = self.aval_duration
            aval_stats["Topples"] = self.topples
            aval_stats["Area"] = self.area
            aval_stats["Lost mass"] = self.lost_mass
            aval_stats["Distance"] = self.distance
        else:
            aval_stats["Duration"] = self.aval_duration[aval_index]
            aval_stats["Topples"] = self.topples[aval_index]
            aval_stats["Area"] = self.area[aval_index]
            aval_stats["Lost mass"] = self.lost_mass[aval_index]
            aval_stats["Distance"] = self.distance[aval_index]

        return aval_stats

    def save_avalanche_stats(self, fname):
        """Creates a dictionary object with all avalanche state and saves it
        all as a pickle file.
        This can be used as creating a file for the Observables class.

        Parameters
        ==========

        fname: string

            Name of output file.

        """

        aval_stats = self.view_avalanche_stats("all")
        aval_stats["Dimensions"] = (self.length, self.width)
        aval_stats["Threshold"] = self.threshold
        aval_stats["Time Elapsed"] = self.time
        aval_stats["Mass History"] = self.mass_history
        aval_stats["Grid"] = self.grid

        pickle.dump(aval_stats, open(fname, "wb"))

        print(f"aval_stats dictionary dumped to {fname}!")
        return aval_stats
