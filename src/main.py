# -*- coding: utf-8 -*-
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
                          QMainWindow, QTableWidgetItem, QVBoxLayout, QWidget)
import qdarkstyle
import sys
from threading import Thread

# Custom functions
from about import AboutUi
import utils
from visual import DynamicMplCanvas

# TODO:
# - Add tooltips
# - Add error checking
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
        self.tab1_pushButton_UpdateNames.clicked.connect(self.tab1_pushButton_Update)


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

        # Add matplotlib widget
        self.vbox         = QVBoxLayout()
        self.MplCanvas    = DynamicMplCanvas()
        self.navi_toolbar = NavigationToolbar(self.MplCanvas, self)
        self.vbox.addWidget(self.MplCanvas)
        self.vbox.addWidget(self.navi_toolbar)
        self.vbox.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.widget_Plot.setLayout(self.vbox)


    #########################
    # TAB 1 DATA: FUNCTIONS #
    #########################

    def tab1_comboBox_updateXYAxis(self):
        """ADD DESCRIPTION"""
        self.comboBox_XAxis.addItems(self.var_names)
        self.comboBox_YAxis.addItems(self.var_names)


    def tab1_tableWidget_comboBox_updateDtype(self):
        """ADD DESCRIPTION"""
        # Find which widget sent the signal and get row location
        clicked_widget = self.sender().parent()
        index          = self.tab1_tableWidget_VariableInfo.indexAt(clicked_widget.pos())
        row            = index.row()
        new_dtype      = \
            self.tab1_tableWidget_VariableInfo.cellWidget(row, 1).findChild(QComboBox).currentText()
        var_name      = self.var_names[row] 

        # Try and update data type
        try:
            if new_dtype == 'datetime': 
                new_var = pd.to_datetime(self.data[var_name])
            else:
                new_var = self.data[var_name].astype(utils.LABEL_TO_DTYPE[new_dtype])

            # Update current data and update lcd displays
            self.data[var_name] = new_var
            self.dtypes         = map(str, self.data.dtypes)
            self.tab1_lcd_updateNumbers()
            self.statusBar.showMessage("Converted %s to data type %s" % (var_name, new_dtype))

        except Exception as e:
            self.statusBar.showMessage("Error changing %s to data type %s" % (var_name, new_dtype))
            utils.message_box(message="Error Changing Data Type",
                              informativeText="Error changing data type of %s to %s" % (var_name, new_dtype),
                              windowTitle="Data Conversion Error",
                              type="error")

            # Set combo box back to data type before attempted conversion
            comboBox = self.tab1_tableWidget_VariableInfo.cellWidget(row, 1).findChild(QComboBox)
            comboBox.setCurrentIndex(comboBox.findText(utils.DTYPE_TO_LABEL[self.dtypes[row]], 
                                                       QtCore.Qt.MatchFixedString))

            return


    def tab1_pushButton_Update(self):
        """ADD DESCRIPTION"""
        utils.message_box(message="NOT IMPLEMENTED",
                          informativeText="WRITE IT",
                          type="information",
                          windowTitle="NOT IMPLEMENTED")
        # # Find which widget sent the signal and get row location
        # clicked_widget = self.sender().parent()
        # index          = self.tab1_tableWidget_VariableInfo.indexAt(clicked_widget.pos())
        # row            = index.row()
        # new_var_name   = \
        #     self.tab1_tableWidget_VariableInfo.item(row, 0).text()
        # if new_var_name: 
        #     self.statusBar.showMessage("Changed variable %s to name %s" % (self.var_names[row], new_var_name))
        #     self.var_names[row] = new_var_name
        # else:
        #     utils.message_box(message="Error Changing Variable Name",
        #                       informativeText="Error changing variable %s to name %s" % (self.var_names[row], new_var_name),
        #                       windowTitle="Invalid Variable Name",
        #                       type="error")
        #     return


    def tab1_lcd_updateNumbers(self):
        """ADD DESCRIPTION"""
        # Update data types
        used_dtypes = set()
        counts = pd.value_counts(self.dtypes)
        for i, dtype in enumerate(counts.index.tolist()):
            if 'int' in dtype:
                self.tab1_lcdNumber_Integer.display(counts[i])
                if 'int' not in used_dtypes: used_dtypes.update(['int'])
            elif 'float' in dtype:
                self.tab1_lcdNumber_Float.display(counts[i])
                if 'float' not in used_dtypes: used_dtypes.update(['float'])
            elif 'date' in dtype or 'M' in dtype:
                self.tab1_lcdNumber_DateTime.display(counts[i])
                if 'date' not in used_dtypes: used_dtypes.update(['date'])
            else:
                self.tab1_lcdNumber_Object.display(counts[i])
                if 'object' not in used_dtypes: used_dtypes.update(['object'])

        # Set data types not used to 0
        if 'int'    not in used_dtypes: self.tab1_lcdNumber_Integer.display(0)
        if 'float'  not in used_dtypes: self.tab1_lcdNumber_Float.display(0)
        if 'date'   not in used_dtypes: self.tab1_lcdNumber_DateTime.display(0)
        if 'object' not in used_dtypes: self.tab1_lcdNumber_Object.display(0)


    class tab1_Thread_LoadData(QtCore.QThread):
        """ADD
        
        Parameters
        ----------
        
        Returns
        -------
        """ 
        # Define signals
        data_signal  = QtCore.Signal(pd.DataFrame)
        error_signal = QtCore.Signal(str)

        def __init__(self, file):
            QtCore.QThread.__init__(self)
            self.file = file

        def __del__(self):
            """ADD DESCRIPTION"""
            self.wait()

        def run(self):
            """ADD DESCRIPTION"""
            try:
                # Get file extension and load data
                _, file_extension = os.path.splitext(self.file)
                if file_extension == '.csv': 
                    data = pd.read_csv(self.file)
                elif file_extension == '.tsv':
                    data = pd.read_table(self.file)
                elif file_extension == '.txt':
                    data = pd.read_csv(self.file, delim_whitespace=True)
                else:
                    pass

                # Add sample ID variable to data and emit data signal
                data.insert(0, 'Sample', np.arange(data.shape[0]).astype('int'))
                self.data_signal.emit(data)

            except Exception as e:
                self.error_signal.emit(str(e))


    def tab1_Slot_LoadData(self, signal):
        """ADD
        
        Parameters
        ----------
        
        Returns
        -------
        """
        if isinstance(signal, pd.DataFrame):
            self.data      = signal
            self.dtypes    = map(str, self.data.dtypes)
            self.var_names = self.data.columns.tolist()
            for var_name, dtype in zip(self.var_names, self.dtypes):
                self.tab1_tableWidget_addRow(var_name, dtype)

            # Update lcd displays and combo boxes for plotting
            self.tab1_lcdNumber_Rows.display(self.data.shape[0])
            self.tab1_lcdNumber_Columns.display(self.data.shape[1])
            self.tab1_lcd_updateNumbers()
            self.tab1_comboBox_updateXYAxis()
            self.statusBar.showMessage("Data loaded with %d rows and %d columns" % \
                                        (self.data.shape))
        else:
            utils.message_box(message="Error Loading Data",
                              informativeText="Error loading file %s because %s" % (self.file, signal),
                              windowTitle="I/O Error",
                              type="error")
            return
        

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
            self.file   = file # Define as attribute for accessing in other functions
            self.thread = self.tab1_Thread_LoadData(file)
            self.thread.data_signal.connect(self.tab1_Slot_LoadData)
            self.thread.error_signal.connect(self.tab1_Slot_LoadData)
            self.thread.start()
            

    def tab1_tableWidget_addRow(self, var_name, dtype):
        """Adds new row to a table widget

        Parameters
        ----------

        Returns
        -------
        None
        """
        # Define cell widget and name of variable
        cell_widget = QWidget()
        name_item   = QTableWidgetItem(var_name)

        # Make 'Sample' variable not editable
        if var_name == 'Sample':
            name_item.setFlags(QtCore.Qt.ItemIsEnabled)
        else:
            name_item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)

        # Insert row
        name_item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        idx = self.tab1_tableWidget_VariableInfo.rowCount()
        self.tab1_tableWidget_VariableInfo.insertRow(idx)
        self.tab1_tableWidget_VariableInfo.setItem(idx, 0, name_item)

        # Define combox box and populate
        if var_name != 'Sample':
            combo_box = QComboBox()
            for value in utils.DTYPE_TO_LABEL.itervalues(): combo_box.addItem(value)
            combo_box.setCurrentIndex(combo_box.findText(utils.DTYPE_TO_LABEL[dtype], 
                                                         QtCore.Qt.MatchFixedString))
            combo_box.currentIndexChanged.connect(self.tab1_tableWidget_comboBox_updateDtype)

            # Define a horizontal layout, format, and add to row
            layout = QHBoxLayout(cell_widget)
            layout.addWidget(combo_box)
            layout.setAlignment(QtCore.Qt.AlignCenter)
            layout.setContentsMargins(0, 0, 0, 0)
            cell_widget.setLayout(layout)
            self.tab1_tableWidget_VariableInfo.setCellWidget(idx, 1, cell_widget)
        
        else:
            fixed_item = QTableWidgetItem('integer')
            fixed_item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.tab1_tableWidget_VariableInfo.setItem(idx, 1, fixed_item)


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