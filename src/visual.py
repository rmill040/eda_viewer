# -*- coding: utf-8 -*-
from __future__ import print_function

# Set matplotlib backend to PySide
import matplotlib
matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4'] = 'PySide'
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


    def _reset_plots(self):
        """ADD DESCRIPTION"""
        try:
            self.fig.delaxes(self.axes)
            self.axes = self.fig.add_subplot(111)
        except:
            pass

        try:
            self.fig.delaxes(self.axes_x)
            self.fig.delaxes(self.axes_y)
            self.axes = self.fig.add_subplot(111)
        except:
            pass


    def update_plot(self, sample, x, y, xlabel, ylabel, plot_type, plot_generated):
        """ADD
        
        Parameters
        ----------
        
        Returns
        -------
        """
        # Clear plotting canvas
        self._reset_plots()
        try:
            # Scatter plot
            if plot_type == 'Scatter':
                title_str = "Scatter: {} x {}".format(xlabel, ylabel)
                self.axes.scatter(x, y)
                self.axes.set_xlabel(xlabel)
                self.axes.set_ylabel(ylabel)
                self.axes.set_title(title_str)

            # Line plot
            elif plot_type == 'Line':
                title_str = "Line: {} x {}".format(xlabel, ylabel)
                self.axes.plot(x, y)
                self.axes.set_xlabel(xlabel)
                self.axes.set_ylabel(ylabel)
                self.axes.set_title(title_str)
            
            # Scatter + Line plot
            elif plot_type == 'Scatter + Line':
                title_str = "Scatter + Line: {} x {}".format(xlabel, ylabel)
                self.axes.plot(x, y, '-o')
                self.axes.set_xlabel(xlabel)
                self.axes.set_ylabel(ylabel)
                self.axes.set_title(title_str)
            
            # Histogram
            elif plot_type == 'Histogram':
                if x is not None: self.axes.hist(x, alpha=.6, label=xlabel, color='blue')
                if y is not None: self.axes.hist(y, alpha=.6, label=ylabel, color='green')
                
                # Add labels and title
                if x is not None and y is not None:
                    title_str = "Histogram: {} and {}".format(xlabel, ylabel)
                    self.axes.set_xlabel(xlabel + ' and ' + ylabel)
                
                elif x is not None and y is None:
                    title_str = "Histogram: {}".format(xlabel)
                    self.axes.set_xlabel(xlabel)
                
                else:
                    title_str = "Histogram: {}".format(ylabel)
                    self.axes.set_xlabel(ylabel)

                # Set title for any histogram
                self.axes.set_title(title_str)
                self.axes.set_ylabel('Value')
                plt.legend()


            # Bar Chart
            elif plot_type == 'Bar Chart':
                xlabel = 'Sample'
                if x is not None: self.axes.bar(sample, x, alpha=.6, label=xlabel, color='blue')
                if y is not None: self.axes.bar(sample, y, alpha=.6, label=ylabel, color='green')

                # Add labels and title
                if x is not None and y is not None:
                    title_str = "Bar Chart: {} and {}".format(xlabel, ylabel)
                
                elif x is not None and y is None:
                    title_str = "Bar Chart: {}".format(xlabel)
                
                else:
                    title_str = "Bar Chart: {}".format(ylabel)

                # Set title for any bar chart
                self.axes.set_title(title_str)
                self.axes.set_xlabel(xlabel)
                self.axes.set_ylabel('Value')
                plt.legend()

            # Boxplot
            else:
                if x is not None and y is None:
                    title_str = "Boxplot: {}".format(xlabel)
                    self.axes.boxplot(x)
                    self.axes.set_ylabel('Value')
                    self.axes.set_title(title_str)

                elif x is None and y is not None: 
                    title_str = "Boxplot: {}".format(ylabel)
                    self.axes.boxplot(y)
                    self.axes.set_ylabel('Value')
                    self.axes.set_title(title_str)

                else:
                    self.fig.delaxes(self.axes)

                    # X variable
                    self.axes_x = self.fig.add_subplot(121)
                    self.axes_x.boxplot(x)
                    self.axes_x.set_ylabel("Value")
                    self.axes_x.set_title("Boxplot: {}".format(xlabel))

                    # Y variable
                    self.axes_y = self.fig.add_subplot(122)
                    self.axes_y.boxplot(y)
                    self.axes_y.set_title("Boxplot: {}".format(ylabel))

            # Create better layout then draw
            plt.tight_layout()
            self.draw()
            plot_generated[0] = True # This lets main UI know the plot generated
            return 'Success'

        except Exception as e:
            plot_generated[0] = False
            return str(e)


    def add_predictions_to_plot(self):
        """ADD
        
        Parameters
        ----------
        
        Returns
        -------
        """
        pass
