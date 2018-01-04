from __future__ import division, print_function

__description__= \
"""
Helper functions for application
""".strip()

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
from sklearn.metrics import (accuracy_score, calinski_harabaz_score, mean_squared_error, 
                             silhouette_score)
from sklearn.model_selection import KFold, StratifiedKFold
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC, SVR
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor


###############
"""CONSTANTS"""
###############

AUTHOR         = "Robert Milletich"
VERSION        = "0.0.1"
BUILT_WITH     = "PySide (1.2.4) + Python (2.7.13)"
LICENSE        = "https://github.com/rmill040/eda_viewer/blob/master/LICENSE"
WEBSITE        = "https://github.com/rmill040/eda_viewer"

MAIN_DIR       = os.path.abspath(__file__).split('src')[0]
UI_PATH        = os.path.join(os.path.join(MAIN_DIR, 'src'), 'gui.ui')
ICONS_PATH     = os.path.join(MAIN_DIR, 'icons')
print(ICONS_PATH)
USE_DARK_THEME = True
PLOTS_FOR_PRED = ['Scatter', 'Line', 'Scatter + Line']
N_SPLITS       = 3

DTYPE_TO_LABEL = {'int64': 'integer', 
                  'float64': 'float',
                  'object': 'object',
                  'datetime64[ns]': 'datetime'}
LABEL_TO_DTYPE = {value: key for key, value in DTYPE_TO_LABEL.iteritems()}

LINK_MODEL_API = {
    'Classification': {
        'Random Forests':         'http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html',
        'K-Nearest Neighbors':    'http://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html',
        'Support Vector Machine': 'http://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html',
        'Neural Network':         'http://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html',
        'Gaussian Process':       'http://scikit-learn.org/stable/modules/generated/sklearn.gaussian_process.GaussianProcessClassifier.html',
        'Linear Model':           'http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html',
        'Extra Trees':            'http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.ExtraTreesClassifier.html',
        'Gradient Boosting':      'http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingClassifier.html',
        'Decision Tree':          'http://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html'
    },
    'Regression': {
        'Random Forests':         'http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html',
        'K-Nearest Neighbors':    'http://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsRegressor.html',
        'Support Vector Machine': 'http://scikit-learn.org/stable/modules/generated/sklearn.svm.SVR.html',
        'Neural Network':         'http://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPRegressor.html',
        'Gaussian Process':       'http://scikit-learn.org/stable/modules/generated/sklearn.gaussian_process.GaussianProcessRegressor.html',
        'Linear Model':           'http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html',
        'Extra Trees':            'http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.ExtraTreesRegressor.html',
        'Gradient Boosting':      'http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingRegressor.html',
        'Decision Tree':          'http://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeRegressor.html'
    },
    'Clustering': {
        'K-Means':       'http://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html',
        'DBSCAN':        'http://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html',
        'Agglomerative': 'http://scikit-learn.org/stable/modules/generated/sklearn.cluster.AgglomerativeClustering.html'
    }
}