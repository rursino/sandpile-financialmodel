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

        self.grid = np.zeros((length, width), dtype=int) + int(threshold / 2)
        self.demand = np.zeros((length, width), dtype=int)

        # Track the overall number of units of the sandpile overtime.
        # The grid will store the volume at each time step.
        self.volume_history = []

        # Track the time of the course of the sandpile.
        self.time = 0

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
        self.volume_history.append(self.volume())
        self.threshold += 0.001

    def volume(self):
        """Return the volume of the grid."""

        return np.sum(self.grid)

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
                                        loc=0.5*self.threshold,
                                        scale=0.2*self.threshold
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

        p = 1 - stats.powerlaw.cdf(x=np.arange(units*0.05),
                                a = 0.1,
                                loc = 0,
                                scale = units
                                )
        p = np.concatenate([p, 0.0 + np.zeros(int(units*0.95))])
        p /= sum(p)

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
            weights = self.demand_probability(int(units))
            self.demand[i][j] += np.random.choice(events, p=weights)

        return np.sum(self.demand)

    def trade(self):
        """ Execute one trade by updating the demand grid and then realising
        the demands of each investor into their volume of stocks.
        This function also resets the demand of investors back to zero.
        """

        self.update_demand_grid()

        self.grid += self.demand
        self.demand = np.zeros((self.length, self.width), dtype=int)

        self.increment_time()

    def run_simulation(self, duration):
        """ Run a number of trades set by the 'duration' parameter.

        Parameters
        ==========

        duration: int

            The number of trades to execute.

        """

        for _ in range(duration):
            self.trade()

    def save_simulation(self, fname):
        """ Creates a dictionary containing information of the run simulation,
        including the dimensions of the grid, the units of stock owned by
        each investor (from the grid) and a timeseries of the history of the
        grid volume.

        Parameters
        ==========

        fname: string

            Name of output file.

        """

        simulation = {}
        simulation["Dimensions"] = (self.length, self.width)
        simulation["Threshold"] = self.threshold
        simulation["Time Elapsed"] = self.time
        simulation["Volume History"] = self.volume_history
        simulation["Grid"] = self.grid

        pickle.dump(simulation, open(fname, "wb"))

        return simulation
