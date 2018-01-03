# -*- coding: utf-8 -*-

# Import libraries from api
from visual_api import *

# Set plotting style
plt.style.use('seaborn-darkgrid')

# Define colors to use
REG_COLORS   = ['red', 'orange', 'cyan', 'purple', 'teal', 'dodgerblue', 
                'darkgreen', 'darksalmon', 'slategrey']
CLF_COLORS   = [['green', 'red'], ['darkgreen', 'darksalmon'], ['purple', 'orange']]


class MplCanvas(FigureCanvas):
    """Base MPL widget for plotting
    
    Parameters
    ----------

    Returns
    -------
    """
    def __init__(self, parent=None, dpi=100):
        self.fig                      = plt.figure(dpi=dpi)
        self.axes                     = self.fig.add_subplot(111)
        self._reg_predictions_added   = 0
        self._clf_predictions_added   = 0
        self._clust_predictions_added = 0

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)


class DynamicMplCanvas(MplCanvas):
    """A canvas that updates itself on call with a new plot."""
    def __init__(self, *args, **kwargs):
        MplCanvas.__init__(self, *args, **kwargs)
        self.compute_initial_figure()


    def compute_initial_figure(self):
        """Initial demo plot for matplotlib canvas"""
        self.axes.plot([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 
                       [70, 90, 100, 110, 130, 150, 160, 170, 180, 190, 215, 0, 0], '-o',
                       color='green')
        self.axes.set_xlabel("Number of Espresso Shots")
        self.axes.set_ylabel("Heart Rate")
        self.axes.annotate('No more heart rate', xy=(11, 0), xytext=(8, 20), 
                          arrowprops=dict(facecolor='black', shrink=0.05))
        self.axes.set_ylim([-2, 220])
        self.axes.set_title("Demo Plot: Number of Espresso Shots x Heart Rate")
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


    def update_plot(self, sample, x, y, xlabel, ylabel, plot_type, plot_generated, checkbox):
        """ADD
        
        Parameters
        ----------
        
        Returns
        -------
        """
        # Clear plotting canvas and define variables used for plotting
        self._reset_plots() 
        self.x = x
        self.y = y

        try:
            # Scatter plot
            if plot_type == 'Scatter':
                title_str = "Scatter: {} x {}".format(xlabel, ylabel)
                self.axes.scatter(x, y, alpha=.6)
                self.axes.set_xlabel(xlabel)
                self.axes.set_ylabel(ylabel)
                self.axes.set_title(title_str)

            # Line plot
            elif plot_type == 'Line':
                title_str = "Line: {} x {}".format(xlabel, ylabel)
                self.axes.plot(x, y, alpha=.6)
                self.axes.set_xlabel(xlabel)
                self.axes.set_ylabel(ylabel)
                self.axes.set_title(title_str)
            
            # Scatter + Line plot
            elif plot_type == 'Scatter + Line':
                title_str = "Scatter + Line: {} x {}".format(xlabel, ylabel)
                self.axes.plot(x, y, '-o', alpha=.6)
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
                plt.legend(loc='best')


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
                plt.legend(loc='best')

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

            # Update plot status
            plot_generated['status'] = True # This lets main UI know the plot generated
            plot_generated['xlabel'] = xlabel
            plot_generated['ylabel'] = ylabel

            # Enable/disable checkbox based on plot types
            if plot_type in utils.PLOTS_FOR_PRED:
                checkbox.setEnabled(True)
                checkbox.setChecked(True)
            else:
                checkbox.setEnabled(False)
                checkbox.setChecked(False)

            return 'Success'

        except Exception as e:
            plot_generated['status'] = False # Sorry about your luck :(
            plot_generated['xlabel'] = 'None'
            plot_generated['ylabel'] = 'None'
            return str(e)


    def add_predictions_to_plot(self, y_pred, model_type, model_name):
        """ADD
        
        Parameters
        ----------
        
        Returns
        -------
        """
        try:
            if model_type == 'Regression':
                if self._reg_predictions_added > (len(REG_COLORS)-1): self._reg_predictions_added = 0
                
                self.axes.scatter(self.x, y_pred, label='Predicted: {}'.format(model_name),
                                  color=REG_COLORS[self._reg_predictions_added], alpha=.6)
                self._reg_predictions_added += 1
            
            elif model_type == 'Classification':
                if self._clf_predictions_added > (len(CLF_COLORS)-1): self._clf_predictions_added = 0
                
                # Plot hits and misses
                hits, misses = np.where(y_pred == self.y)[0], np.where(y_pred != self.y)[0]
                self.axes.scatter(self.x.iloc[hits], y_pred[hits], 
                                  label='Correct: {}'.format(model_name), alpha=.6, facecolors='none', 
                                  edgecolors=CLF_COLORS[self._clf_predictions_added][0])
                self.axes.scatter(self.x.iloc[misses], y_pred[misses], 
                                  label='Incorrect: {}'.format(model_name), alpha=.6, marker='x',
                                  color=CLF_COLORS[self._clf_predictions_added][1])
                self._clf_predictions_added += 1

            else:
                cluster_ids  = np.unique(y_pred)
                CLUST_COLORS = utils.get_spaced_colors(len(cluster_ids)+1, offset=self._clust_predictions_added)

                for i, label in enumerate(cluster_ids):
                    idx = np.where(y_pred == label)[0]
                    self.axes.scatter(self.x.iloc[idx], self.y.iloc[idx], 
                                      label='Cluster {}: {}'.format(i, model_name),
                                      color=next(CLUST_COLORS),
                                      alpha=.6)
                self._clust_predictions_added += 1
            
            # Add legend and draw plot
            plt.legend(loc='upper left')
            self.draw()
            return 'Success'

        except Exception as e:
            return str(e)