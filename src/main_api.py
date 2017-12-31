from __future__ import division, print_function

# Set matplotlib backend to PySide
import matplotlib
matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4'] = 'PySide'
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar

import numpy as np
import os
import pandas as pd
from PySide import QtCore
from PySide.QtGui import (QApplication, QComboBox, QFileDialog, QHBoxLayout, QHeaderView, 
                          QIcon, QMainWindow, QMessageBox, QTableWidgetItem, QVBoxLayout, QWidget)
import qdarkstyle
import sys
from threading import Thread

# Custom functions
from about import AboutUi
import utils
from visual import DynamicMplCanvas