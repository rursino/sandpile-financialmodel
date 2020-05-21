import numpy as np
from itertools import *

grid = np.array([
[1,2,5,2,4],
[3,4,8,5,7],
[7,1,0,2,0],
[4,2,1,8,1],
[0,3,4,2,1]
])

class SandPile():

    def __init__(self, grid):

        self.grid = grid
        self.length = grid.shape[0]
        self.width = grid.shape[1]

    def neighbours(self):

        neighbours_dict = {}

        neighbours = lambda x, y : [(xx, yy) for xx in range(x-1, x+2)
                                       for yy in range(y-1, y+2)
                                       if (-1 < x < self.width and
                                           -1 < y < self.length and
                                           (x != xx or y != yy) and
                                           (0 <= xx < self.width) and
                                           (0 <= yy < self.length))]

        for site in product(*(range(n) for n in (self.length, self.width))):

            i, j = site

            neighbour_vals = []
            for nsite in neighbours(i,j):
                ii, jj = nsite
                neighbour_vals.append(self.grid[ii][jj] - self.grid[i][j])

            neighbours_dict[site] = neighbour_vals

        return neighbours_dict

sp = SandPile(grid)
sp.neighbours()
