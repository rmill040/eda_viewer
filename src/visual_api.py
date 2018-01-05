from __future__ import print_function

__description__= \
"""
Matplotlib plotting functionality for application
""".strip()

# Set matplotlib backend to PySide
import matplotlib
matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4'] = 'PySide'
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from PySide.QtGui import QSizePolicy

import numpy as np
import pandas as pd

# Custom functions
import utils

# Set plotting style
plt.style.use('seaborn-darkgrid')

# Define colors to use
REG_COLORS = ['red', 'orange', 'cyan', 'purple', 'teal', 'dodgerblue', 
                'darkgreen', 'darksalmon', 'slategrey']
CLF_COLORS = [['green', 'red'], ['darkgreen', 'darksalmon'], ['purple', 'orange']]