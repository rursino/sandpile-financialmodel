""" A script that contains the sandpile model to simulate the temporal
behaviour of a stock market index fund.

AIM:
-
"""


""" IMPORTS """

from itertools import *
import numpy as np
import matplotlib.pyplot as plt
import pickle


""" FUNCTIONS """

class SandPile:

    """ THE STOCK MARKET SANDPILE MODEL:
    This program establishes the set of functions to form the basic form of
    the sandpile model that attempts to simulate the stock market and contains
    a set of subroutines for the NxN sandpile grid.

    Details:
    - a "cell" represents an investor that participates in an index fund of a
    stock market.
    - a "grain" represents a unit of stock owned by an investor. When the
    number of grains (or units) changes, it is due to the following events:
        - demand to buy a unit of stock -> buy (+1)
        - demand to sell a unit of stock (-1)
    There is also a choice to do nothing, so the no. of units stays unchanged.
    Each grain (unit) of stock contains some value that does not vary with
    different grains. The value is the price of the unit of stock at a
    particular time.
    - two cells are connected by the involvement of two investors in a trade of
    stock or 'demand' points.

    * Why does a trade occur? Due to randomness or due to some condition?
    * what does a topple represent in the stock market? A sell off from one
    investor?

    """

    def __init__(self, length, width, threshold=4):
        """Initialize a sandpile with the specified length and width."""
        self.length = length
        self.width = width
        self.threshold = threshold

        self.grid = np.zeros((length, width), dtype=int)

        # Give each unit of stock a price.
        self.price = 10

        # Track the overall number of units of the sandpile overtime.
        # The grid will store the masses at each time step.
        self.mass_history = []

        # Track the time of the course of the sandpile.
        self.time = 0

        # Record the observables of each crash.
        self.crash_duration = []
        self.num_of_crashes = 0
        self.price_drop = 0
        self.topples = []
        self.lost_mass = []

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

    def drop_units(self, n=1, cell=None):
        """Add `n` units of stock to the grid.  Each unit is added to
        a random cell (or site).

        This function also increments the time by 1 and update the internal
        `mass_history`.  Depending on how you want to code things, you may wish
        to also run the crash (alternatively, the crash might be
        executed elsewhere).

        Parameters
        ==========

        n: int

          The number of units of stock of drop at this time step.  If left
          unspecified, defaults to 1.

        cell: tuple (i,j)

          The cell on which the unit(s) should be dropped.  If `None`,
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

    def crash(self):
        """Run the crash causing all cells to topple and store the stats of
        the crash in the appropriate variables.
        For extended sandpile, crashes are run when the difference between
        any cell and any of its neighbours reaches a threshold.

        Parameters
        ==========

        name: string

            Given name for the crash.

        """

        # Initialize crash statistics.
        num_of_topples = 0
        toppled_cells = []
        start_mass = self.mass()
        start_time = self.time

        # Record first toppled cell for calculation of distance.
        first_toppled_cell = []

        # Topple cells until all cells have less than the threshold no.
        cells_to_topple = self.check_threshold()
        while cells_to_topple:
            # Topple each cell and update crash statistics.
            for cell in cells_to_topple:
                self.topple(cell)

                if not first_toppled_cell:
                    first_toppled_cell.append(cell[0])
                    first_toppled_cell.append(cell[1])

                toppled_cells.append(cell)
                num_of_topples += 1

            cells_to_topple = self.check_threshold()

            self.time += 1

        # Record observables into the crash_stats attributes
        unique_toppled_cells = np.unique(toppled_cells, axis=0)

        # Calculate 'area' = number of unique toppled cells.
        area = len(unique_toppled_cells)

        # Calculate distance.
        difference_i = unique_toppled_cells.T[0] - first_toppled_cell[0]
        difference_j = unique_toppled_cells.T[1] - first_toppled_cell[1]
        distance = abs(difference_i) + abs(difference_j)
        max_distance = max(distance)

        # Record all stats into crash_stats.
        self.crash_duration.append(self.time - start_time)
        self.num_of_crashes += 1
        self.topples.append(num_of_topples)
        self.area.append(area)
        self.lost_mass.append(start_mass - self.mass())
        self.distance.append(max_distance)

    def view_crash_stats(self, crash_index):
        """View the stats of any crash or all crashes.

        Parameters
        ==========

        crash_index: int or string

            Index of lists to get any crash, or 'all' gives entirety of
            all lists.

        """

        crash_stats = {}

        if crash_index == "all":
            crash_stats["Duration"] = self.crash_duration
            crash_stats["Topples"] = self.topples
            crash_stats["Area"] = self.area
            crash_stats["Lost mass"] = self.lost_mass
            crash_stats["Distance"] = self.distance
        else:
            crash_stats["Duration"] = self.crash_duration[crash_index]
            crash_stats["Topples"] = self.topples[crash_index]
            crash_stats["Area"] = self.area[crash_index]
            crash_stats["Lost mass"] = self.lost_mass[crash_index]
            crash_stats["Distance"] = self.distance[crash_index]

        return crash_stats

    def save_crash_stats(self, fname):
        """Creates a dictionary object with all crash state and saves it
        all as a pickle file.
        This can be used as creating a file for the Observables class.

        Parameters
        ==========

        fname: string

            Name of output file.

        """

        crash_stats = self.view_crash_stats("all")
        crash_stats["Dimensions"] = (self.length, self.width)
        crash_stats["Threshold"] = self.threshold
        crash_stats["Time Elapsed"] = self.time
        crash_stats["Mass History"] = self.mass_history
        crash_stats["Grid"] = self.grid

        pickle.dump(crash_stats, open(fname, "wb"))

        return crash_stats
