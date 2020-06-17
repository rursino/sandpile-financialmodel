""" Development of the demand grid and its association with the trade market
and crash scenarios.
"""


""" IMPORTS """
import numpy as np
import scipy as sp
from scipy import stats
import matplotlib.pyplot as plt
from itertools import *


""" INPUTS """
length = 5
width = 5
threshold = 50


""" FUNCTIONS """

class StockMarket:

    def __init__(self, length, width, threshold):
        """Initialize a sandpile with the specified length and width."""
        self.length = length
        self.width = width
        self.threshold = threshold

        self.grid = np.zeros((length, width), dtype=int) + int(threshold / 2)
        self.demand = np.zeros((length, width), dtype=int)

        # Give each unit of stock a price.
        self.price = 10

        # Track the overall number of units of the sandpile overtime.
        # The grid will store the volume at each time step.
        self.volume_history = []

        # Track the time of the course of the sandpile.
        self.time = 0

        # Record the observables of each crash.
        self.crash_duration = []
        self.num_of_crashes = 0
        self.price_drop = 0
        self.lost_volume = []
        self.uninvolved_investors = []

    def volume(self):
        """Return the volume of the grid."""

        return np.sum(self.grid)

    def increment_time(self):
        """ Call this function to record the mass whenever there is an increment
        of time added to the course of the sandpile.
        """
        self.time += 1
        self.volume_history.append(np.sum(self.grid))
        self.threshold += 0.005

    def demand_probability(self, units, threshold):
        hold = 0.2

        if units == 0:
            sell, buy = 0, 1 - hold
        else:
            p = (1 - hold) * stats.norm.cdf(x=units,
                                        loc=0.9*threshold,
                                        scale=0.15*threshold
                                        )
            sell, buy = p, (1 - hold) - p

        return sell, buy, hold

    def magnitude_probability(self, units):
        """
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
        """
        """

        for cell in product(range(self.length), range(self.width)):
            i, j = cell
            units = self.grid[i][j]

            events = self.magnitude_probability(int(units)) * np.array([-1, 1, 0])
            weights = self.demand_probability(units, self.threshold)
            self.demand[i][j] += np.random.choice(events, p=weights)

        return np.sum(self.demand)

    def execute_trades(self):
        """
        """

        self.update_demand_grid()

        self.grid += self.demand
        self.demand = np.zeros((length, width), dtype=int)

        self.increment_time()

    def DEV_execute_trades(self):
        """Executes trades from information in demand grid abd returns the
        cells that were not paired for trading. These cells either lost or
        gained a unit of stock without it being moved to or from another
        investor (i.e. the volume of units changed).
        """

        self.update_demand_grid()

        buy_cells = list(zip(*np.where(self.demand > 0)))
        sell_cells = list(zip(*np.where(self.demand < 0)))

        choice_set = []

        difference = len(buy_cells) - len(sell_cells)
        if difference != 0:
            if difference > 0:
                primary_set, secondary_set = buy_cells, sell_cells
            elif difference < 0:
                primary_set, secondary_set = sell_cells, buy_cells

            choice_indices = list(range(len(primary_set)))
            while len(choice_indices) > len(secondary_set):
                choice_index = np.random.choice(choice_indices)
                choice_set.append(primary_set[choice_index])
                choice_indices.remove(choice_index)

        self.grid += self.demand
        self.demand = np.zeros((length, width), dtype=int)

        self.increment_time()

        if difference < 0: #This is a crash, no matter how small.
            self.uninvolved_investors.append(len(choice_set))

    def crash(self, increment_time=False, duration=100):
        """
        """
        start_volume = self.volume()
        start_time = self.time

        for _ in range(duration):
            self.execute_trades()

        self.lost_volume.append(start_volume - self.volume())
        self.crash_duration.append(self.time - start_time)
        self.num_of_crashes += 1

    def DEV_crash(self, increment_time=False):
        """
        """

        start_volume = self.volume()
        start_time = self.time
        uninvolved = []

        while True:
            uninvolved_cells = self.execute_trades(increment_time)
            for cell in uninvolved_cells:
                uninvolved.append(cell)

        unique_uninvolved = np.unique(uninvolved, axis=0)

        self.lost_volume.append(start_volume - self.volume())
        self.crash_duration.append(self.time - start_time)
        self.num_of_crashes += 1
        self.uninvolved_investors.append(len(unique_uninvolved))




""" EXECUTION """
market = StockMarket(length, width, threshold)
market.grid

market.crash(duration=2000)
plt.plot(market.volume_history)#; plt.xlim([500,2000]); plt.ylim([1000,1450])

market.grid

market.update_demand_grid()
buy_cells = list(zip(*np.where(market.demand > 0)))
sell_cells = list(zip(*np.where(market.demand < 0)))

buy_cells
sell_cells

get_units = lambda i, j: market.demand[i][j]

get_units(*(2,4))

market.demand

for buy_cell, sell_cell in product(buy_cells, sell_cells):
    if get_units(*buy_cell) == -get_units(*sell_cell):
        transfer_units = get_units(*buy_cell)

        market.grid[buy_cell[0]][buy_cell[1]] += transfer_units
        market.demand[buy_cell[0]][buy_cell[1]] -= transfer_units

        market.demand[sell_cell[0]][sell_cell[1]] += transfer_units
        market.grid[sell_cell[0]][sell_cell[1]] -= transfer_units

        try:
            buy_cells.remove(buy_cell)
            sell_cells.remove(sell_cell)
        except ValueError():
            pass

        print(buy_cell, sell_cell, "transfered", transfer_units)

buy_cells
sell_cells

market.demand

for _ in range(50):
    market.execute_trades()

plt.plot(market.volume_history)
market.grid


""" DEVS """
n = 50
x = np.arange(0, n+1)
y = 0.8 * stats.norm.cdf(x=x,
                        loc=0.9*n,
                        scale=0.15*n
                        )
plt.plot(x, y); plt.plot(x, 0.8-y)

units = 50
p = 1 - stats.powerlaw.cdf(x=np.arange((1/5)*units),
                        a = 0.03,
                        loc = 0,
                        scale = units
                        )
p /= sum(p)
p = np.concatenate([p, np.zeros(int((4/5)*units))])
len(p)
plt.plot(p); plt.xlim([0, units])

np.random.choice(units, p=p)
np.arange(4.5)
