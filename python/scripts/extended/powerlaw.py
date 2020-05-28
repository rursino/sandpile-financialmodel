"""Development of the power law curve fit to pdf's of observables.
"""

from itertools import *
import numpy as np
import scipy as sp
from scipy import spatial, stats
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

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


ob = Observables("./../../output/sandpile_10_10_1000.pik")

ob.powerlaw_fit(ob.area, 1, "log", "log")

x = np.array(ob.distance)
y = np.array(ob.topples)
plt.plot(x,y)
plt.yscale("linear")


ob.regression(x, y, type="powerlaw", remove_zeroes=0, plot=1)
