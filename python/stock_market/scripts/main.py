""" Execution of stock market sandpile.
"""


""" IMPORTS """
import numpy as np

import sys
sys.path.append("./core/")
import sandpile

from importlib import reload
reload(sandpile)


""" INPUTS """
length = 50
width = 50


""" SETUP """
market = sandpile.StockMarket(length, width)


""" FUNCTIONS """
def main():
    market.grid


""" EXECUTION """
if __name__ == "__main__":
    main()
