""" Program establishes a set of subroutines for the NxN sandpile grid.
"""

from itertools import *
import numpy as np
import scipy as sp
from scipy import spatial, stats
import matplotlib.pyplot as plt
import seaborn as sns
import pickle


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
        for vals in neighbours:
            np.any(neighbours[vals] <= -self.threshold)

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


class Observables:

    def __init__(self, data):
        """This class loads avalanche observables and provides analytic
        functionals and visualisations.
        """
        data = pickle.load(open(data, "rb"))
        self.data = data

        self.aval_duration = self.data["Duration"]
        self.topples = self.data["Topples"]
        self.area = self.data["Area"]
        self.lost_mass = self.data["Lost mass"]
        self.distance = self.data["Distance"]

        self.length = self.data["Dimensions"][0]
        self.width = self.data["Dimensions"][1]
        self.threshold = self.data["Threshold"]
        self.grid = self.data["Grid"]

        self.time_elapsed = self.data["Time Elapsed"]
        self.mass_history = self.data["Mass History"]

    def histogram(self, stat, density=False):
        """ Produces a histogram or probability distribution of any observable.

        Parameters
        =========

        stat: attribute

            Observable to plot.

        density: bool, optional

            If True, histogram is normalised to a probability distribution.
            If False, histogram is plotted.

            Defaults to False.
        """

        if density:
            title = "Probability Distribution"
        else:
            title = "Histogram"

        fig, ax = plt.subplots(figsize=(20,10))
        ax.hist(stat, density=density, bins=25)
        ax.set_title(title)
        ax.set_xlabel("Value")
        ax.set_ylabel("Frequency")

    def distpdf(self, stat, hist=False):
        """ Produces a probability distribution line plot of any observable.

        Parameters
        =========

        stat: attribute

            Observable to plot.

        hist: bool, optional

            If True, a histogram is plotted with the distribution plot.
            If False, just the distribution pdf is plotted.

            Defaults to False.
        """

        plt.figure(figsize=(20,10))
        sns.distplot(stat, hist=hist, bins=25)
        plt.title("Probability Distribution")
        plt.xlabel("Value")
        plt.ylabel("Frequency")

    def line_plot(self, stat):
        """ Produces a line plot of any observable.

        Parameters
        =========

        stat: attribute

            Observable to plot.

        """

        fig, ax = plt.subplots(figsize=(20,10))
        ax.plot(stat)
        ax.set_title("Line Plot")

    def visualise_grid(self, *args, **kwargs):
        """ Produces a heatmap of the grid. """

        plt.figure(figsize=(20,15))
        sns.heatmap(self.grid, xticklabels=False, yticklabels=False,
        *args, **kwargs)

    def powerlaw_fit(self, data, plot=False, xscale="linear", yscale="linear"):
        """Fits a power law equation to a probability distribution function
        with slope = b and intercept = log10(c).

        Parameters
        ==========

        data: array-like

            1-D array to produce frequency distribution and fit power law
            equation.

        plot: bool, optional

            If True, generates a line plot of x vs. y and of the regression
            equation.

            Other parameters include: "loglog", "semilogx", "semilogy", which
            generates line plots with respective log and linear axis scales.

            Defaults to False.

        xscale, yscale: str, optional

            Axis scale of the x-axis and y-axis, respectively.

        """

        x, y = np.unique(data, return_counts=1)

        return self.regression(x, y, "powerlaw", 0, plot, xscale, yscale)



    def regression(self, x, y, type="linear", remove_zeroes=False, plot=False,
    xscale="linear", yscale="linear"):
        """Regresses two variables, with added functionality to enable power
        law regression (see below).

        Returns:

            slope, intercept, r-value

        Parameters
        ==========

        x, y: list-like

            Two variables to regress. x is independent, y is dependent.

        type: str, optional

            The type of regression to perform.

            "linear":  performs linear regression with equation fit y = b*x + c,
            where slope = b and intercept = c.

            "powerlaw": performs powerlaw regression with equation fit
            y = c*(x^b), where slope = b and intercept = log10(c).
            The equation is linearised by takeing log10 on both sides to get
            log10(y) = log10(c) + b * log10(x).

            Defaults to "linear".

        remove_zeroes: bool, optional

            If True, gathers indices of x and y where x = 0 and removes the
            values from x and y with these indices.
            This is useful for removing zeroes in data when performing powerlaw
            regressions.

            Defaults to False.

        plot: bool, optional

            If True, generates a line plot of x vs. y and of the regression
            equation.

            Other parameters include: "loglog", "semilogx", "semilogy", which
            generates line plots with respective log and linear axis scales.

            Defaults to False.

        xscale, yscale: str, optional

            Axis scale of the x-axis and y-axis, respectively.

        """

        if remove_zeroes:
            x = x[[i for i in range(len(x)) if x[i]!=0]]
            y = y[[i for i in range(len(x)) if x[i]!=0]]

        if type == "linear":
            x = np.array(x)
            y = np.array(y)
        elif type == "powerlaw":
            x = np.log10(x)
            y = np.log10(y)

        regression = stats.linregress(x, y)

        if plot:
            b, c = regression[:2]

            fig = plt.figure(figsize=(20,10))

            if type == "linear":
                plt.scatter(x, y)
                plt.plot(x, (b*x + c), color='r')
            elif type == "powerlaw":
                plt.scatter(10**x, 10**y)
                plt.plot(10**x, 10**(b*x + c), color='r')
                c = 10**c

            plt.xscale(xscale)
            plt.yscale(yscale)

        return regression[:3]
