"""Development of the wind function/s."""


""" IMPORTS """
import numpy as np
import matplotlib.pyplot as plt
from itertools import *


""" INPUTS """
grid = np.array([
[1,4,2,4,5],
[0,1,6,3,1],
[3,5,8,2,1],
[2,1,0,0,7],
[9,1,4,3,5]
])


""" FUNCTIONS """
class SandPile():

    def __init__(self, grid):

        self.grid = grid
        self.length = grid.shape[0]
        self.width = grid.shape[1]

    def wind(self, direction, speed):
        """Moves sand grains along the grid with specified direction.

        Parameters
        ==========

        direction: str

            Direction of wind. Takes either L, R, U or D.

        speed: int

            Amount of grains moved to its neighbour grid.

        """

        if direction == "R":
            for i in range(self.length):
                for j in range(self.width):
                    if self.grid[i][j] >=  speed:
                        self.grid[i][j] -= speed
                        if j < self.width - 1:
                            self.grid[i][j+1] += speed

        elif direction == "D":
            for i in range(self.length):
                for j in range(self.width):
                    if self.grid[i][j] >=  speed:
                        self.grid[i][j] -= speed
                        if i < self.length - 1:
                            self.grid[i+1][j] += speed

        elif direction == "L":
            for i in range(self.length):
                for j in range(self.width):
                    if self.grid[i][j] >=  speed:
                        self.grid[i][j] -= speed
                        if j > 0:
                            self.grid[i][j-1] += speed

        elif direction == "U":
            for i in range(self.length):
                for j in range(self.width):
                    if self.grid[i][j] >=  speed:
                        self.grid[i][j] -= speed
                        if i > 0:
                            self.grid[i-1][j] += speed

""" EXECUTION """
sp = SandPile(grid)
sp.wind("R", 2)
