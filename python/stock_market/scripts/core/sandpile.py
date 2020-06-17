""" A script that contains the sandpile model to simulate the temporal
behaviour of a stock market index fund.
"""


""" IMPORTS """

from itertools import *
import numpy as np
import scipy as sp
from scipy import stats
import matplotlib.pyplot as plt
import pickle


""" FUNCTIONS """

class StockMarket:

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
    - a "topple" represents a set of trade of one unit of stock from an
    investor demanding to sell and an investor demanding to buy.
        - An investor is more likely to sell a unit of stock if it is more
        units and more likely to buy if it has fewer units.
        - The amount of units an investor may wish to buy or sell also depends
        on a probability dependent on the amount of units the investor owns.
        - a 'demand' table collects the details of every investors demand
        points.
        - two cells are connected by the involvement of two investors in a
        trade of stock or 'demand' points.

    """

    def __init__(self, length, width, threshold=4):
        """Initialize a sandpile with the specified length and width."""
        self.length = length
        self.width = width
        self.threshold = threshold

        self.grid = np.zeros((length, width), dtype=int) + 2
        self.demand = np.zeros((length, width), dtype=int)

        # Track the overall number of units of the sandpile overtime.
        # The grid will store the volume at each time step.
        self.volume_history = []

        # Track the time of the course of the sandpile.
        self.time = 0

        # Record the observables of each crash.
        self.crash_duration = []
        self.num_of_crashes = 0
        self.lost_volume = []

    def plot_volume(self, start_time=None, end_time=None):
        """ Plots the volume of the grid over its lifetime.

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
        volume = np.array(self.volume_history)[start_time:end_time]

        plt.plot(time, volume)

    def increment_time(self):
        """ Call this function to record the mass whenever there is an increment
        of time added to the course of the sandpile.
        """
        self.time += 1
        self.volume_history.append(np.sum(self.grid))
        self.threshold += 0.005

    def volume(self):
        """Return the volume of the grid."""

        return np.sum(self.grid)

    def average_volume(self):
        """Return the average volume (or height) of the grid."""

        return (np.sum(self.grid))/(self.length * self.width)

    def demand_probability(self, units):
        """ Determine the probability of an investor selling, buying and
        holding stock, which depends on the number of units the investor
        currently holds and the threshold set from the initialisation of the
        stock market sandpile.

        Parameters
        ==========

        units: int

            The number of units an investor (cell) holds.

        """

        hold = 0.2

        if units == 0:
            sell, buy = 0, 1 - hold
        else:
            p = (1 - hold) * stats.norm.cdf(x=units,
                                        loc=0.9*self.threshold,
                                        scale=0.15*self.threshold
                                        )
            sell, buy = p, (1 - hold) - p

        return sell, buy, hold

    def magnitude_probability(self, units):
        """ Determine the probability of an investor moving an amount of stock,
        no matter how it is moved (sold or bought), which depends on the number
        of units the investor currently holds.

        Parameters
        ==========

        units: int

            The number of units an investor (cell) holds.

        """

        p = 1 - stats.powerlaw.cdf(x=np.arange(units*0.25),
                                a = 0.01,
                                loc = 0,
                                scale = units
                                )
        p /= sum(p)
        p = np.concatenate([p, np.zeros(int(units*0.75))])

        return np.random.choice(units, p=p)

    def update_demand_grid(self):
        """ Update the demand of each investor at a particular time. Each
        investor will either sell, buy or hold stock according to the
        probability distribution set by the number of units one holds. The
        number of units one buys or sells can also depend on the probability
        distribution set by the number of units one holds
        """

        for cell in product(range(self.length), range(self.width)):
            i, j = cell
            units = self.grid[i][j]

            events = self.magnitude_probability(int(units)) * np.array([-1, 1, 0])
            weights = self.demand_probability(units, self.threshold)
            self.demand[i][j] += np.random.choice(events, p=weights)

        return np.sum(self.demand)

    def trade(self):
        """ Execute one trade by updating the demand grid and realising the
        demands of each investor into their volume of stocks.
        This function also resets the demand of investors back to zero.
        """

        self.update_demand_grid()

        self.grid += self.demand
        self.demand = np.zeros((length, width), dtype=int)

        self.increment_time()

    def run_trades(self, duration):
        """ Run a number of trades set by the 'duration' parameter.

        Parameters
        ==========

        duration: int

            The number of trades to execute.

        """
        start_volume = self.volume()
        start_time = self.time

        for _ in range(duration):
            self.trade()

        self.lost_volume.append(start_volume - self.volume())
        self.crash_duration.append(self.time - start_time)
        self.num_of_crashes += 1

    def detect_crashes(self):
        """
        """

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
            crash_stats["Lost volume"] = self.lost_volume
            crash_stats["Distance"] = self.distance
        else:
            crash_stats["Duration"] = self.crash_duration[crash_index]
            crash_stats["Topples"] = self.topples[crash_index]
            crash_stats["Area"] = self.area[crash_index]
            crash_stats["Lost volume"] = self.lost_volume[crash_index]
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
        crash_stats["Volume History"] = self.volume_history
        crash_stats["Grid"] = self.grid

        pickle.dump(crash_stats, open(fname, "wb"))

        return crash_stats
