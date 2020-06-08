"""This program establishes the set of functions to provide analytics and
visualisations of avalanche stats from run experiments of the sandpile model.
"""

""" IMPORTS """

import numpy as np
from scipy import spatial, stats
import matplotlib.pyplot as plt
import seaborn as sns
import pickle


""" FUNCTIONS """

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

    def histogram(self, stat, density=False):
        """ Produces a histogram or probability distribution of any observable.

        Parameters
        =========

        stat: attribute

            Observable to plot.

        density: bool, optional

            If True, histogram is normalised to a probability distribution.
            If False, histogram is plotted.

            Defaults to False.
        """

        if density:
            title = "Probability Distribution"
        else:
            title = "Histogram"

        fig, ax = plt.subplots(figsize=(20,10))
        ax.hist(stat, density=density, bins=25)
        ax.set_title(title)
        ax.set_xlabel("Value")
        ax.set_ylabel("Frequency")

    def distpdf(self, stat, hist=False):
        """ Produces a probability distribution line plot of any observable.

        Parameters
        =========

        stat: attribute

            Observable to plot.

        hist: bool, optional

            If True, a histogram is plotted with the distribution plot.
            If False, just the distribution pdf is plotted.

            Defaults to False.
        """

        plt.figure(figsize=(20,10))
        sns.distplot(stat, hist=hist, bins=25)
        plt.title("Probability Distribution")
        plt.xlabel("Value")
        plt.ylabel("Frequency")

    def line_plot(self, stat):
        """ Produces a line plot of any observable.

        Parameters
        =========

        stat: attribute

            Observable to plot.

        """

        fig, ax = plt.subplots(figsize=(20,10))
        ax.plot(stat)
        ax.set_title("Line Plot")

    def visualise_grid(self, *args, **kwargs):
        """ Produces a heatmap of the grid. """

        plt.figure(figsize=(20,15))
        sns.heatmap(self.grid, xticklabels=False, yticklabels=False,
        *args, **kwargs)

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
            x = [x[i] for i in range(len(x)) if x[i]!=0]
            y = [y[i] for i in range(len(x)) if x[i]!=0]

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
