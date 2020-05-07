""" Program establishes a set of subroutines for the NxN sandpile grid.
"""

import numpy as np
import scipy as sp
import scipy.spatial
import matplotlib.pyplot as plt
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
        self.radius = []

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

    def drop_sand(self, n=1, site=None):
        """Add `n` grains of sand to the grid.  Each grains of sand is added to
        a random site.

        This function also increments the time by 1 and update the internal
        `mass_history`.  Depending on how you want to code things, you may wish
        to also run the avalanche (alternatively, the avalanching might be
        executed elsewhere).

        Parameters
        ==========

        n: int

          The number of grains of sand of drop at this time step.  If left
          unspecified, defaults to 1.

        site: tuple (i,j)

          The site on which the grain(s) of sand should be dropped.  If `None`,
          a random site is used.

        """

        if site:
            i,j = site
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

    def topple(self, site, increment_time=False):
        """Topple the specified site.

        Parameters
        ==========

        site: tuple-like

            The address of the site to topple.

        increment_time: bool

            Whether to increment one time step or not. Defaults to False.

        """

        i, j = site

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
        """Run the avalanche causing all sites to topple and store the stats of
        the avalanche in the appropriate variables.

        Parameters
        ==========

        name: string

            Given name for the avalanche.

        """

        # Initialize avalanche statistics.
        num_of_topples = 0
        toppled_sites = []
        start_mass = self.mass()
        start_time = self.time

        # Record first toppled site for calculation of radius.
        first_toppled_site = []

        # Topple sites until all sites have less than the threshold no.
        while np.any(self.grid >= 4):
            # Extact sites to topple.
            topple_locations = np.where(self.grid >= 4)
            all_i = topple_locations[0]
            all_j = topple_locations[1]

            if not first_toppled_site:
                first_toppled_site.append(all_i[0])
                first_toppled_site.append(all_j[0])

            # Topple each site and update avalanche statistics.
            for topple_number in range(len(all_i)):

                site = (all_i[topple_number], all_j[topple_number])

                SandPile.topple(self, site)

                num_of_topples += 1
                toppled_sites.append(site)

            self.time += 1

        # Record observables into the avalanche_stats attributes
        unique_toppled_sites = np.unique(toppled_sites, axis=0)

        # Calculate 'area' = number of unique toppled sites.
        area = len(unique_toppled_sites)

        # Calculate radius.
        difference_i = unique_toppled_sites.T[0] - first_toppled_site[0]
        difference_j = unique_toppled_sites.T[1] - first_toppled_site[1]
        radii = np.sqrt(difference_i**2 + difference_j**2)
        max_radius = max(radii)

        # Record all stats into avalanche_stats.
        self.aval_duration.append(self.time - start_time)
        self.num_of_avalanches += 1
        self.topples.append(num_of_topples)
        self.area.append(area)
        self.lost_mass.append(start_mass - self.mass())
        self.radius.append(max_radius)

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
            aval_stats["Radius"] = self.radius
        else:
            aval_stats["Duration"] = self.aval_duration[aval_index]
            aval_stats["Topples"] = self.topples[aval_index]
            aval_stats["Area"] = self.area[aval_index]
            aval_stats["Lost mass"] = self.lost_mass[aval_index]
            aval_stats["Radius"] = self.radius[aval_index]

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

        aval_stats = SandPile.view_avalanche_stats(self, "all")
        aval_stats["Dimensions"] = (self.length, self.width)
        aval_stats["Threshold"] = self.threshold
        aval_stats["Time Elapsed"] = self.time
        aval_stats["Mass History"] = self.mass_history
        aval_stats["Grid"] = self.grid

        pickle.dump(aval_stats, open(fname, "wb"))

        print(f"aval_stats dictionary dumped to {fname}!")
        return aval_stats


class Observables:

    def __init__(self, fname):
        """This class loads avalanche observables and provides analytic
        functionals and visualisations.
        """
        self.data = pickle.load(open(fname, "rb"))

        self.aval_duration = self.data["Duration"]
        self.topples = self.data["Topples"]
        self.area = self.data["Area"]
        self.lost_mass = self.data["Lost mass"]
        self.radius = self.data["Radius"]

        self.length = self.data["Dimensions"][0]
        self.width = self.data["Dimensions"][1]
        self.threshold = self.data["Threshold"]
        self.grid = self.data["Grid"]

        self.time_elapsed = self.data["Time Elapsed"]
        self.mass_history = self.data["Mass History"]

    def histogram(self, stat):
        """ Produces a histogram of any observable. """

        fig, ax = plt.subplots()
        ax.hist(stat)
        ax.set_title("Histogram")
        ax.set_xlabel("Value")
        ax.set_ylabel("Frequency")

    def prob_dist(self, stat):
        """ Produces a probability distribution of any observable. """

        raise NotImplementedError()

    def line_plot(self, stat):
        """ Produces a line plot of any observable. """

        fig, ax = plt.subplots()
        ax.plot(stat)
        ax.set_title("Line Plot")

    def visualise_grid(self, *args, **kwargs):
        """ Produces a heatmap of the grid. """

        plt.imshow(self.grid, *args, **kwargs)
