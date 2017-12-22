# -*- coding: utf-8 -*-

from __future__ import division, print_function

import os
import pandas as pd
from PySide import QtCore
from PySide.QtGui import (QApplication, QComboBox, QFileDialog, QHBoxLayout, QHeaderView, 
                          QMainWindow, QTableWidgetItem, QWidget)
import qdarkstyle
import sys

# Custom functions
from about import AboutUi
import utils

# TODO:
# - Fix coloring of icon on AboutUi
# - Add tooltips
# - Add error checking
# - Add About UI
# - Add message box popups
# - Add threading (maybe make decorator?)
# - Add keyboard shortcuts
# - Add zoom for hyperparameters text box (https://stackoverflow.com/questions/7987881/how-to-scale-zoom-a-qtextedit-area-from-a-toolbar-button-click-and-or-ctrl-mou)
# - Finish adding functions and connecting


class MainUi(QMainWindow):
    """ADD DESCRIPTION HERE"""
    def __init__(self, parent=None):

        #######################
        # PRELIMINARY ACTIONS #
        #######################

        # Parent constructor
        QMainWindow.__init__(self, parent)

        # Load .ui file dynamically for now
        utils.load_ui(utils.UI_PATH, self)

        # Set window title, status bar, and force tab widget to open on data tab
        self.setWindowTitle('Exploratory Data Analysis Viewer')
        self.statusBar.showMessage("""Click "Load Data" button to begin""")
        self.tabWidget_Analysis.setCurrentIndex(0)

        # Populate combo box for model names
        self.model_type = self.tab3_comboBox_ModelType.currentText()
        self.tab3_comboBox_ModelName.addItems(utils.LINK_MODEL_API[self.model_type].keys())

        # Activate URL for model API links
        self.model_name = self.tab3_comboBox_ModelName.currentText()
        self.url = utils.LINK_MODEL_API[self.model_type][self.model_name]
        self.tab3_label_LinkToModelAPI.setOpenExternalLinks(True)
        self.tab3_label_LinkToModelAPI.setText(
            '''<a href='{}'>Link to Model API</a>'''.format(self.url)
            )

        # Add model parameters to plain text widget
        self.clf = utils.get_model(model_name=self.model_name, model_type=self.model_type)
        text = utils.pretty_print_dict(self.clf.get_params())
        self.tab3_plainTextEdit_ModelParameters.setPlainText(text)


        ########################
        # CONNECT FILE MENU UI #
        ########################

        # Exit button (TODO: ADD ARE YOU SURE BEFORE EXITING)
        self.menuItem_Exit.triggered.connect(self.close)

        self.menuItem_About.triggered.connect(AboutUi)


        #############################
        # CONNECT TAB 1 DATA TAB UI #
        #############################

        self.tab1_pushButton_LoadData.clicked.connect(self.tab1_pushButton_Load)


        ###################################
        # CONNECT TAB 2 UNIVARIATE TAB UI #
        ###################################



        ###############################
        # CONNECT TAB 3 BIVARIATE TAB #
        ###############################

        self.tab3_comboBox_ModelType.activated[str].connect(self.tab3_comboBox_addModelNames)
        self.tab3_comboBox_ModelType.activated[str].connect(self.tab3_label_setLink)
        self.tab3_comboBox_ModelType.activated[str].connect(self.tab3_plainTextEdit_setModelParams)

        self.tab3_comboBox_ModelName.activated[str].connect(self.tab3_label_setLink)
        self.tab3_comboBox_ModelName.activated[str].connect(self.tab3_plainTextEdit_setModelParams)


        ########################
        # CONNECT VISUALIZE UI #
        ########################



    #########################
    # TAB 1 DATA: FUNCTIONS #
    #########################

    def tab1_comboBox_updateXYAxis(self):
        """ADD DESCRIPTION"""
        self.comboBox_XAxis.addItems(self.data.columns)
        self.comboBox_YAxis.addItems(self.data.columns)


    def tab1_lcd_updateNumbers(self):
        """ADD DESCRIPTION"""
        # Update rows and columns 
        self.tab1_lcdNumber_Rows.display(self.data.shape[0])
        self.tab1_lcdNumber_Columns.display(self.data.shape[1])

        # Update data types
        counts = pd.value_counts(self.dtypes)
        for i, dtype in enumerate(counts.index.tolist()):
            if 'int' in dtype:
                self.tab1_lcdNumber_Integer.display(counts[i])
            elif 'float' in dtype:
                self.tab1_lcdNumber_Float.display(counts[i])
            elif 'date' in dtype or 'M' in dtype:
                self.tab1_lcdNumber_DateTime.display(counts[i])
            else:
                self.tab1_lcdNumber_Object.display(counts[i])


    def tab1_pushButton_Load(self):
        """ADD DESCRIPTION"""
        # File dialog options for opening single file
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file, _ = QFileDialog.getOpenFileName(self, "Load: Data", "/",
                                              "*.csv files (*.csv);;"
                                              "*.tsv files (*tsv);;"
                                              "*.txt files (*.txt);;",
                                              options=options)

        # If a file is selected, try and open
        if file:
            try:
                self.file         = file
                _, file_extension = os.path.splitext(file)
                if file_extension == '.csv': 
                    self.data = pd.read_csv(self.file)
                elif file_extension == '.tsv':
                    self.data = pd.read_table(self.file)
                elif file_extension == '.txt':
                    self.data = pd.read_csv(self.file, delim_whitespace=True)
                else:
                    pass

            except Exception as e:
                pass

            try:
                # Add rows to table with data types
                self.dtypes    = map(str, self.data.dtypes)
                self.var_names = self.data.columns.tolist()
                for var_name, dtype in zip(self.var_names, self.dtypes):
                    self.tab1_tableWidget_addRow(var_name, dtype)

                self.tab1_lcd_updateNumbers()
                self.tab1_comboBox_updateXYAxis()
                self.statusBar.showMessage("Data loaded with %d rows and %d columns" % \
                                            (self.data.shape))
            
            except Exception as e:
                pass


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


    ##############################
    # TAB 3 BIVARIATE: FUNCTIONS #
    ##############################

    def tab3_comboBox_addModelNames(self):
        """ADD DESCRIPTION"""
        self.model_type = self.tab3_comboBox_ModelType.currentText()
        self.tab3_comboBox_ModelName.clear()
        self.tab3_comboBox_ModelName.addItems(utils.LINK_MODEL_API[self.model_type].keys())


    def tab3_label_setLink(self):
        """ADD DESCRIPTION"""
        self.model_type = self.tab3_comboBox_ModelType.currentText()
        self.model_name = self.tab3_comboBox_ModelName.currentText()
        self.url = utils.LINK_MODEL_API[self.model_type][self.model_name]
        self.tab3_label_LinkToModelAPI.setText(
            '''<a href='{}'>Link to Model API</a>'''.format(self.url)
            )

    def tab3_plainTextEdit_setModelParams(self):
        """ADD DESCRIPTION"""
        self.clf = utils.get_model(model_name=self.model_name, model_type=self.model_type)
        text = utils.pretty_print_dict(self.clf.get_params())
        self.tab3_plainTextEdit_ModelParameters.setPlainText(text)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    if utils.USE_DARK_THEME: app.setStyleSheet(qdarkstyle.load_stylesheet())
    window = MainUi()
    window.showMaximized()
    sys.exit(app.exec_())