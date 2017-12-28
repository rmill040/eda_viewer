# -*- coding: utf-8 -*-
from __future__ import division, print_function

from collections import OrderedDict
import json
import numpy as np
import os
import pandas as pd
from PySide.QtCore import QFile, QMetaObject
from PySide.QtGui import QMessageBox
from PySide.QtUiTools import QUiLoader
import scipy.stats as ss
from sklearn.cluster import AgglomerativeClustering, DBSCAN, KMeans
from sklearn.ensemble import (ExtraTreesClassifier, ExtraTreesRegressor,
                              GradientBoostingClassifier, GradientBoostingRegressor,
                              RandomForestClassifier, RandomForestRegressor)
from sklearn.gaussian_process import GaussianProcessClassifier, GaussianProcessRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.svm import SVC, SVR
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor


###############
"""CONSTANTS"""
###############

AUTHOR         = "Robert Milletich"
VERSION        = "0.0.1"
BUILT_WITH     = "PySide + Python 2.7"
LICENSE        = "https://github.com/rmill040/eda_viewer/blob/master/LICENSE"
WEBSITE        = "https://github.com/rmill040/eda_viewer"

UI_PATH        = os.path.join(os.path.abspath(__file__).split('utils.py')[0], 'gui.ui')
USE_DARK_THEME = True

DTYPE_TO_LABEL = {'int64': 'integer', 
                  'float64': 'float',
                  'object': 'object',
                  'datetime64[ns]': 'datetime'}
LABEL_TO_DTYPE = {value: key for key, value in DTYPE_TO_LABEL.iteritems()}
LINK_MODEL_API = {
    'Classification': {
        'Random Forests': 'http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html',
        'K-Nearest Neighbors': 'http://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html',
        'Support Vector Machine': 'http://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html',
        'Neural Network': 'http://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html',
        'Gaussian Process': 'http://scikit-learn.org/stable/modules/generated/sklearn.gaussian_process.GaussianProcessClassifier.html',
        'Linear Model': 'http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html',
        'Extra Trees': 'http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.ExtraTreesClassifier.html',
        'Gradient Boosting': 'http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingClassifier.html',
        'Decision Tree': 'http://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html'
    },
    'Regression': {
        'Random Forests': 'http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html',
        'K-Nearest Neighbors': 'http://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsRegressor.html',
        'Support Vector Machine': 'http://scikit-learn.org/stable/modules/generated/sklearn.svm.SVR.html',
        'Neural Network': 'http://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPRegressor.html',
        'Gaussian Process': 'http://scikit-learn.org/stable/modules/generated/sklearn.gaussian_process.GaussianProcessRegressor.html',
        'Linear Model': 'http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html',
        'Extra Trees': 'http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.ExtraTreesRegressor.html',
        'Gradient Boosting': 'http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingRegressor.html',
        'Decision Tree': 'http://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeRegressor.html'
    },
    'Clustering': {
        'K-Means': 'http://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html',
        'DBSCAN': 'http://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html',
        'Agglomerative': 'http://scikit-learn.org/stable/modules/generated/sklearn.cluster.AgglomerativeClustering.html'
    }
}


######################
"""HELPER FUNCTIONS"""
######################

class UiLoader(QUiLoader):
    """ADD DESCRIPTION"""
    def __init__(self, base_instance):
        QUiLoader.__init__(self, base_instance)
        self.base_instance = base_instance

    def createWidget(self, class_name, parent=None, name=''):
        """ADD
        
        Parameters
        ----------
        
        Returns
        -------
        """
        if parent is None and self.base_instance:
            return self.base_instance
        else:
            # create a new widget for child widgets
            widget = QUiLoader.createWidget(self, class_name, parent, name)
            if self.base_instance: setattr(self.base_instance, name, widget)
            return widget


def load_ui(ui_file, base_instance=None):
    """ADD
    
    Parameters
    ----------
    
    Returns
    -------
    """
    loader = UiLoader(base_instance)
    widget = loader.load(ui_file)
    QMetaObject.connectSlotsByName(widget)
    return widget


def get_model(model_name, model_type):
    """ADD
    
    Parameters
    ----------
    
    Returns
    -------
    """
    models = {
        'Classification': {
            'Random Forests': RandomForestClassifier,
            'K-Nearest Neighbors': KNeighborsClassifier,
            'Support Vector Machine': SVC,
            'Neural Network': MLPClassifier,
            'Gaussian Process': GaussianProcessClassifier,
            'Linear Model': LinearRegression,
            'Extra Trees': ExtraTreesClassifier,
            'Gradient Boosting': GradientBoostingClassifier,
            'Decision Tree': DecisionTreeClassifier
        },
        'Regression': {
            'Random Forests': RandomForestRegressor,
            'K-Nearest Neighbors': KNeighborsRegressor,
            'Support Vector Machine': SVR,
            'Neural Network': MLPRegressor,
            'Gaussian Process': GaussianProcessRegressor,
            'Linear Model': LogisticRegression,
            'Extra Trees': ExtraTreesRegressor,
            'Gradient Boosting': GradientBoostingRegressor,
            'Decision Tree': DecisionTreeRegressor
            },
        'Clustering': {
            'K-Means': KMeans,
            'DBSCAN': DBSCAN,
            'Agglomerative': AgglomerativeClustering
        }
    }

    return models[model_type][model_name]()


def pretty_print_dict(model_params):
    """ADD
    
    Parameters
    ----------
    
    Returns
    -------
    """
    if 'pooling_func' in model_params.keys(): 
        model_params = {k:v for k,v in model_params.items() if k != 'pooling_func'}

    return json.dumps(model_params, indent=4)


def message_box(message, informativeText, windowTitle, type, question=False):
    """ADD
    
    Parameters
    ----------
    
    Returns
    -------
    """
    msg = QMessageBox()
    msg.setText(message)
    msg.setInformativeText(informativeText)
    msg.setWindowTitle(windowTitle)

    if type == "warning":
        msg.setIcon(QMessageBox.Warning)
    elif type == "error":
        msg.setIcon(QMessageBox.Critical)
    else:
        msg.setIcon(QMessageBox.Information)

    if question:
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        msg.exec_()
    else:
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


def univariate_statistics(data):
    """ADD
    
    Parameters
    ----------
    
    Returns
    -------
    """
    results = OrderedDict()
    if 'int' in str(data.dtypes) or 'float' in str(data.dtypes):
        results['Mean']     = np.mean(data)
        results['Median']   = np.median(data)
        results['Variance'] = np.var(data)
        results['SD']       = np.std(data)
        results['Skewness'] = ss.skew(data)
        results['Kurtosis'] = ss.kurtosis(data)
        results['CV']       = results['SD']/results['Mean']
        results['Minimum']  = np.min(data)
        results['Maximum']  = np.max(data)
        results['P 0.5%']   = np.percentile(data, 0.5)
        results['P 2.5%']   = np.percentile(data, 2.5)
        results['P 25%']    = np.percentile(data, 25)
        results['P 75%']     = np.percentile(data, 75)
        results['P 97.5%']  = np.percentile(data, 97.5)
        results['P 99.5%']  = np.percentile(data, 99.5)
        results['IQR']      = results['P 75%'] - results['P 25%']

        # # Format string
        # results_str = '-'*28
        # results_str += '\n{:<15}{:<15}\n'.format('Statistic', 'Value')
        # results_str += '-'*28
        # results_str += '\n'
        # for key, value in results.iteritems():
        #     results_str += '{:<15}{:<15.3f}'.format(key, value)
        #     if key != 'IQR': results_str += '\n'
        # results_str += '\n'
        # results_str += '-'*28

    else:
        results['Unique']  = len(np.unique(data))
        results['Mode']    = ss.mode(data)[0]
        results['Minimum'] = np.min(data)
        results['Maximum'] = np.max(data)

        # # Format string
        # results_str = '-'*28
        # results_str += '\n{:<15}{:<15}\n'.format('Statistic', 'Value')
        # results_str += '-'*28
        # results_str += '\n'
        # for key, value in results.iteritems():
        #     results_str += '{:<15}{:<15.3f}'.format(key, value)
        #     if key != 'Maximum': results_str += '\n'
        # results_str += '\n'
        # results_str += '-'*28

    return results


def is_numeric(data):
    """ADD
    
    Parameters
    ----------
    
    Returns
    -------
    """
    if 'int' in str(data.dtypes) or 'float' in str(data.dtypes):
        return 1
    else:
        return 0


def value_counts_grouped(data, value_counts):
    """ADD
    
    Parameters
    ----------
    
    Returns
    -------
    """
    # Calculate counts and bins
    counts, bins  = np.histogram(data, bins='doane')
    n_bins        = len(bins)

    # Create grouped frequency table
    index, values = [], []
    for i in xrange(n_bins-1):

        # Last interval is closed
        if i == (n_bins-2):
            index.append(
                '[{:.3f}, {:.3f}]'.format(bins[i], bins[i+1])
                )
        
        # Other intervals are half-open (open to left, closed to right)
        else:
            index.append(
                '[{:.3f}, {:.3f})'.format(bins[i], bins[i+1])
                )
        
        values.append(counts[i])

    return pd.DataFrame(values, columns=['Count'], index=index)





if __name__ == "__main__":
    dat = pd.DataFrame(np.arange(100), columns=['x1'])
    #univariate_statistics(dat['x1'])
    print(value_counts_grouped(dat, pd.value_counts(dat['x1'])))