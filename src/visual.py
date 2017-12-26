# -*- coding: utf-8 -*-
from __future__ import print_function

# Set matplotlib backend to PySide
import matplotlib
matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4']='PySide'
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from PySide import QtCore
from PySide.QtGui import QApplication, QSizePolicy, QVBoxLayout, QWidget

# Custom functions
from utils import message_box

# Set plotting style
plt.style.use('seaborn-darkgrid')


class MplCanvas(FigureCanvas):
    """Base MPL widget for plotting
    
    Parameters
    ----------

    Returns
    -------
    """
    def __init__(self, parent=None, dpi=100):
        self.fig  = plt.figure(dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


class DynamicMplCanvas(MplCanvas):
    """A canvas that updates itself on call with a new plot."""
    def __init__(self, *args, **kwargs):
        MplCanvas.__init__(self, *args, **kwargs)
        self.compute_initial_figure()


    def compute_initial_figure(self):
        """ADD DESCRIPTION"""
        self.axes.scatter([0, 1, 2, 3], [1, 1, 1, 1])
        self.axes.set_xlabel("None")
        self.axes.set_ylabel("None")
        self.axes.set_title("Scatter Plot: None x None")
        plt.tight_layout()


    def update_plot(self, sample, x, y, xlabel, ylabel, plot_type):
        """ADD
        
        Parameters
        ----------
        
        Returns
        -------
        """
        self.axes.clear()

        # Scatter plot
        if plot_type == 'Scatter':
            self.axes.scatter(x, y)
            title_str = "Scatter: {} x {}".format(xlabel, ylabel)
        
        # Line plot
        elif plot_type == 'Line':
            self.axes.plot(x, y)
            title_str = "Line: {} x {}".format(xlabel, ylabel)
        
        # Scatter + Line plot
        elif plot_type == 'Scatter + Line':
            self.axes.plot(x, y, '-o')
            title_str = "Scatter + Line: {} x {}".format(xlabel, ylabel)
        
        # Histogram
        elif plot_type == 'Histogram':
            if x is not None: self.axes.hist(x, alpha=.6, label=xlabel)
            if y is not None: self.axes.hist(y, alpha=.6, label=ylabel)
            plt.legend()
            if x is not None and y is not None:
                title_str = "Histogram: {} and {}".format(xlabel, ylabel)
            if x is not None and y is None:
                title_str = "Histogram: {}".format(xlabel)
            else:
                title_str = "Histogram: {}".format(ylabel)

        # Bar Chart
        elif plot_type == 'Bar Chart':
            xlabel = 'Sample'
            if x is not None: self.axes.bar(sample, x, alpha=.6, label=xlabel)
            if y is not None: self.axes.bar(sample, y, alpha=.6, label=ylabel)
            plt.legend()
            if x is not None and y is not None:
                title_str = "Bar Chart: {} and {}".format(xlabel, ylabel)
            if x is not None and y is None:
                title_str = "Bar Chart: {}".format(xlabel)
            else:
                title_str = "Bar Chart: {}".format(ylabel)

        # Boxplot
        else:
            if x is not None and y is None:
                self.axes.boxplot(x)
                title_str = "Boxplot: {}".format(xlabel)
            if x is None and y is not None: 
                self.axes.boxplot(y)
                title_str = "Boxplot: {}".format(ylabel)
            if x is not None and y is not None:
                message_box(message="Warning: Only Plotting %s" % xlabel,
                            informativeText="Boxplots for both x and y not implemented yet",
                            windowTitle="Warning: Not Implemented",
                            type="warning")
                self.axes.boxplot(x)
                title_str = "Boxplot: {}".format(xlabel)


        # Set labels, title, and layout
        self.axes.set_xlabel(xlabel)
        self.axes.set_ylabel(ylabel)
        self.axes.set_title(title_str)
        plt.tight_layout()
        self.draw()


    def add_predictions_to_plot(self):
        """ADD
        
        Parameters
        ----------
        
        Returns
        -------
        """
        pass
