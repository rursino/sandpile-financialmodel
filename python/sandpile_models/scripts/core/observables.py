"""This program establishes the set of functions to provide analytics and
visualisations of avalanche stats from run experiments of the sandpile model.
"""

""" IMPORTS """

import numpy as np
from scipy import spatial, stats
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
from collections import namedtuple
import copy


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

        # X-axis label for observables.
        self.xlabels = {
        'aval_duration': 'Avalanche Duration (time steps)',
        'topples': 'No. of topples',
        'area': 'No. of toppled cells',
        'lost_mass': 'Total mass lost (grains) ',
        'distance': 'Avalanche Distance',
        'mass_history': 'Mass (grains)'
        }

    def histogram(self, observable, density=False):
        """ Produces a histogram or probability distribution of any observable.

        Parameters
        =========

        observable: str

            Observable to plot.

        density: bool, optional

            If True, histogram is normalised to a probability distribution.
            If False, histogram is plotted.

            Defaults to False.
        """

        data = getattr(self, observable)

        fig, ax = plt.subplots(figsize=(20,10))
        ax.hist(data, density=density, bins=25)

        observable_title = (observable
                .replace('_', ' ')
                .title()
                )
        if density:
            title = f"Probability Distribution: {observable_title}"
            ylabel = "Probability"
        else:
            title = f"Histogram: {observable_title}"
            ylabel = "Frequency"

        ax.set_title(title, fontsize=28)
        ax.set_xlabel(self.xlabels[observable], fontsize=16)
        ax.set_ylabel(ylabel, fontsize=16)

    def distpdf(self, observable, hist=False):
        """ Produces a probability distribution line plot of any observable.

        Parameters
        =========

        observable: str

            Observable to plot.

        hist: bool, optional

            If True, a histogram is plotted with the distribution plot.
            If False, just the distribution pdf is plotted.

            Defaults to False.

        """

        data = getattr(self, observable)

        plt.figure(figsize=(20,10))
        sns.distplot(data, hist=hist, bins=25)

        observable_title = (observable
                .replace('_', ' ')
                .title()
                )
        plt.title(f"Probability Distribution: {observable_title}",
                fontsize=28)
        plt.xlabel(self.xlabels[observable], fontsize=16)
        plt.ylabel("Probability", fontsize=16)

    def line_plot(self, observable):
        """ Produces a line plot of any observable.

        Parameters
        =========

        observable: str

            Observable to plot.

        """

        data = getattr(self, observable)

        fig, ax = plt.subplots(figsize=(20,10))
        ax.plot(data)

        observable_title = (observable
                .replace('_', ' ')
                .title()
                )
        ax.set_title(f"Timeseries: {observable_title}", fontsize=28)
        ax.set_xlabel("Time", fontsize=16)
        ax.set_ylabel(self.xlabels[observable], fontsize=16)

    def visualise_grid(self, *args, **kwargs):
        """ Produces a heatmap of the grid. """

        plt.figure(figsize=(20,15))
        sns.heatmap(self.grid, xticklabels=False, yticklabels=False,
        *args, **kwargs)

    def powerlaw_fit(self, observable, cut=False, plot=False,
                    xscale="linear", yscale="linear"):
        """ Fits a power law equation to a probability distribution function
        with slope = b and intercept = log10(c).

        Parameters
        ==========

        observable: str

            Observable to plot.

        cut: int, optional

            The index to split the (ordered) data to separate the 1/f noise
            from the "log" linear part.
            If False, no split takes place.

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

        data = getattr(self, observable)

        x, y = np.unique(data, return_counts=1)

        x = np.log10(x)
        y = np.log10(y)

        if cut:
            cut_left = (x < cut)
            cut_right = (x >= cut)

            split_xy = ((x[cut_left], y[cut_left]),
                        (x[cut_right], y[cut_right]))
            split_names = iter(("Linear", "Noise"))
        else:
            split_xy = [(x, y)]
            split_names = ()

        fig = plt.figure(figsize=(20,10))
        plt.text(10**0, 10**(len(split_xy)*0.1 + 0.2),
                f"y = a$x^b$", fontsize=18)
        text_position = iter(np.arange(len(split_xy)*0.1, 0.05, -0.1))

        observable_title = (observable
                .replace('_', ' ')
                .title()
                )

        regression_stats = []
        for split_x, split_y in split_xy:

            regression = stats.linregress(split_x, split_y)

            if plot:
                b, c, r = regression[:3]

                plt.plot(10**split_x, 10**split_y)
                y_reg = b*split_x + c
                plt.plot(10**split_x, 10**y_reg, color='r')

                a = 10**c

                plt.xscale(xscale)
                plt.yscale(yscale)

                plt.title(f"Powerlaw fit: {observable_title}", fontsize=28)
                plt.xlabel(self.xlabels[observable], fontsize=16)
                plt.ylabel("Frequency", fontsize=16)

                text_pos = copy.copy(next(text_position))
                reg_text = r"$\bf{" + next(split_names) + "}$: " if split_names else ""
                reg_text += f"a = {a:.2f}, b = {b:.2f}"

                plt.text(10**0.0, 10**text_pos,
                        reg_text,
                        fontsize=14
                        )

                plt.text(10**0.5, 10**text_pos, f"r = {r:.4f}",
                        fontsize=14)

                reg_tuple = namedtuple('reg_tuple', ['a', 'b', 'r'])

                regression_stats.append(reg_tuple(a, b, r))

        return regression_stats
