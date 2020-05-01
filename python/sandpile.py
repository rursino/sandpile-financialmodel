""" Program establishes a set of subroutines for the NxN sandpile grid.
"""

import numpy as np
import scipy as sp
import scipy.spatial
import matplotlib.pyplot as plt


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

        # Record the observables of an avalanche.
        self.avalanche_stats = {}


    def locate(self, i, j):
        """Returns the value of the address (i,j) of the grid.
        Note: address is in array notation, NOT python notation.

        Parameters
        ==========

        i: int

            The row number. Must be between 1 and the length of the grid.


        j: int

            The column number. Must be between 1 and the width of the grid.

        """

        if not (0 < i <= self.length):
            raise ValueError(f"i must be in the range (1, {self.length})")

        if not (0 < j <= self.width):
            raise ValueError(f"j must be in the range (1, {self.width})")

        else:
            return self.grid[i-1][j-1]

    def visualise(self, *args, **kwargs):
        """ Produces a heatmap of the grid.
        """

        plt.imshow(self.grid, *args, **kwargs)

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

    def topple(self, site):
        """Topple the specified site.

        Parameters
        ==========

        site: tuple-like

            The address of the site to topple.

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

    def avalanche(self, name):# Other params: start?
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
        #radius

        # Topple sites until all sites have less than the threshold no.
        while np.any(self.grid >= 4):
            # Extact sites to topple.
            topple_locations = np.where(self.grid >= 4)
            all_i = topple_locations[0]
            all_j = topple_locations[1]

            # Topple each site and update avalanche statistics.
            for topple_number in range(len(all_i)):

                site = (all_i[topple_number], all_j[topple_number])

                SandPile.topple(self, site)

                num_of_topples += 1
                toppled_sites.append(site)
                #length

        # Record observables into the avalanche_stats attributes
        area = len(np.unique(toppled_sites, axis=0))

        avalanche_stat = (self.time,
        num_of_topples,
        area,
        start_mass - self.mass()
        )  #length

        self.avalanche_stats[name] = avalanche_stat
