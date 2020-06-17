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

        x = np.log10(x)
        y = np.log10(y)

        regression = stats.linregress(x, y)

        if plot:
            b, c = regression[:2]

            fig = plt.figure(figsize=(20,10))
            plt.scatter(10**x, 10**y)
            y_reg = b*x + c
            plt.plot(10**x, 10**y_reg, color='r')

            c = 10**c

            plt.xscale(xscale)
            plt.yscale(yscale)

        return regression[:3]
