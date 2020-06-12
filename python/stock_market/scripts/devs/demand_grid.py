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
grid = np.array([
        [79, 76, 80, 75, 78],
        [81, 83, 70, 76, 80],
        [79, 78, 72, 74, 83],
        [80, 73, 79, 74, 84],
        [75, 78, 78, 75, 80]
        ])

threshold = 100


""" FUNCTIONS """

class StockMarket:

    def __init__(self, grid, threshold=threshold):
        """Initialize a sandpile with the specified length and width."""
        self.length = 5
        self.width = 5
        self.threshold = threshold
        self.grid = grid # Hypothetical scenario
        self.demand = np.zeros((5,5), dtype=int)

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
        self.threshold += 0.01

    def demand_probability(self, units, threshold):
        hold = 0.7

        if units == 0:
            sell, buy = 0, 1 - hold
        else:
            p = (1 - hold) * stats.norm.cdf(x=units,
                                        loc=0.75*threshold,
                                        scale=0.15*threshold
                                        )
            sell, buy = p, (1 - hold) - p

        return sell, buy, hold

    def points_probability(units, threshold):
        """
        """

        raise NotImplementedError()

    def update_demand_grid(self):
        """
        """

        for cell in product(range(self.length), range(self.width)):
            i, j = cell
            units = self.grid[i][j]

            events = [-1, 1, 0]
            weights = self.demand_probability(units, self.threshold)
            self.demand[i][j] += np.random.choice(events, p=weights)

        return np.sum(self.demand)

    def execute_trades(self):
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
        self.demand = np.zeros((5,5), dtype=int)

        self.increment_time()

        if difference < 0: #This is a crash, no matter how small.
            self.uninvolved_investors.append(len(choice_set))

    def crash(self, increment_time=False):
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
market = StockMarket(grid)
market.grid

for _ in range(3000):
    market.execute_trades()

market.grid
plt.plot(market.volume_history); plt.ylim([1750, 2700])

""" DEVS """
n = 100
x = np.arange(0, n+1)
y = 0.8 * stats.norm.cdf(x=x,
                        loc=0.75*n,
                        scale=0.15*n
                        )
plt.plot(x, y); plt.plot(x, 0.8-y)
