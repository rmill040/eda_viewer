from __future__ import division, print_function

import pandas as pd
from PySide import QtCore
from PySide.QtGui import (QApplication, QComboBox, QFileDialog, QHBoxLayout,
                         QHeaderView, QMainWindow, QTableWidgetItem, QWidget)
import qdarkstyle
import sys

# Custom functions
import core
import utils


class Ui(QMainWindow):
    """ADD DESCRIPTION HERE"""
    def __init__(self, parent=None):

        #######################
        # PRELIMINARY ACTIONS #
        #######################

        # Parent constructor
        QMainWindow.__init__(self, parent)

        # Load .ui file dynamically for now
        utils.load_ui(utils.UI_PATH, self)

        # Set window title
        self.setWindowTitle('Exploratory Data Analysis Viewer')


        ########################
        # CONNECT FILE MENU UI #
        ########################

        # Exit button (TODO: ADD ARE YOU SURE BEFORE EXITING)
        self.menuItem_Exit.triggered.connect(self.close)


        #######################
        # CONNECT DATA TAB UI #
        #######################

        self.tab1_pushButton_LoadData.clicked.connect(self.tab1_pushButton_Load)

        # Test data here
        self.tab1_tableWidget_addRow('X1', 'int64')
        self.tab1_tableWidget_addRow('X2', 'float64')
        self.tab1_tableWidget_addRow('X3', 'datetime64[ns]')


        #############################
        # CONNECT UNIVARIATE TAB UI #
        #############################



        #########################
        # CONNECT BIVARIATE TAB #
        #########################



        ########################
        # CONNECT VISUALIZE UI #
        ########################



    #########################
    # TAB 1 DATA: FUNCTIONS #
    #########################

    def tab1_pushButton_Load(self):
        """ADD
        
        Parameters
        ----------
        
        Returns
        -------
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file, _ = QFileDialog.getOpenFileName(self, "Load: Data", "/",
                                              "*.csv files (*.csv);;"
                                              "*.tsv files (*tsv);;"
                                              "*.txt files (*.txt);;",
                                              options=options)
        # TODO: ADD READ DATA FUNCTIONS HERE



    def tab1_tableWidget_addRow(self, name, dtype):
        """Adds new row to a table widget

        Parameters
        ----------

        Returns
        -------
        None
        """
        # Define a cell widget and combo box for datatypes 
        cell_widget = QWidget()
        combo_box   = QComboBox()

        # Populate combo box and set value to current dtype
        for value in utils.DTYPES_MAPPING.itervalues(): combo_box.addItem(value)
        combo_box.setCurrentIndex(combo_box.findText(utils.DTYPES_MAPPING[dtype], 
                                                     QtCore.Qt.MatchFixedString))

        # Define a horizontal layout and format
        layout = QHBoxLayout(cell_widget)
        layout.addWidget(combo_box)
        layout.setAlignment(QtCore.Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        cell_widget.setLayout(layout)

        # Add variable name
        name_item = QTableWidgetItem(name)
        name_item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)
        name_item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        # Add data to table widget
        idx = self.tab1_tableWidget_VariableInfo.rowCount()
        self.tab1_tableWidget_VariableInfo.insertRow(idx)
        self.tab1_tableWidget_VariableInfo.setItem(idx, 0, name_item)
        self.tab1_tableWidget_VariableInfo.setCellWidget(idx, 1, cell_widget)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    if utils.USE_DARK_THEME: app.setStyleSheet(qdarkstyle.load_stylesheet())
    window = Ui()
    window.showMaximized()
    sys.exit(app.exec_())