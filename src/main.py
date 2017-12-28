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
                          QMainWindow, QMessageBox, QTableWidgetItem, QVBoxLayout, QWidget)
import qdarkstyle
import sys
from threading import Thread

# Custom functions
from about import AboutUi
import utils
from visual import DynamicMplCanvas

# TODO:
# - Add tooltips (use Designer)
# - Add error checking (consider making separate helper functions to check data configuration)
# - Add status bar updates where necessary
# - Add functionality for machine learning (use Threading)
# - Add keyboard shortcuts
# - Add threading for summary statistics (large samples may freeze main thread for a second or so)
# - Add loading bars where appropriate
# - Add zoom for hyperparameters text box (https://stackoverflow.com/questions/7987881/how-to-scale-zoom-a-qtextedit-area-from-a-toolbar-button-click-and-or-ctrl-mou)
# - Connect all menu item buttons
# - Automatically generate two subplots when two variables are specified for boxplots
# - Add other univariate statistics for tab 2 
#   variance, skewness, kurtosis, coefficient of variation, CIs, IQR
# - Try better printing for tab 2 univariate statistics
# - Build freeze scripts for different operating systems
# - Unit tests


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

        # Enable add headers for table widgets
        self.tab1_tableWidget_VariableInfo.horizontalHeader().setVisible(True)
        self.tab2_tableWidget_Xstats.horizontalHeader().setVisible(True)
        self.tab2_tableWidget_Ystats.horizontalHeader().setVisible(True)
        self.tab2_tableWidget_Xfreq.horizontalHeader().setVisible(True)
        self.tab2_tableWidget_Yfreq.horizontalHeader().setVisible(True)


        ################
        # FILE MENU UI #
        ################

        # Reset data button
        self.menuItem_ResetData.triggered.connect(self.reset)

        # Exit button (TODO: ADD ARE YOU SURE BEFORE EXITING)
        self.menuItem_Exit.triggered.connect(self.exit)
        self.menuItem_About.triggered.connect(AboutUi)


        #####################
        # TAB 1 DATA TAB UI #
        #####################

        # Connect load data button
        self.data_loaded = False
        self.tab1_pushButton_LoadData.clicked.connect(self.load_data)

        # Connect variable names in table widget to item changed signal so that when
        # user changes the label, the app automatically updates other components with 
        # new variable name. The self.already_changed attribute is a "hack" that helps control
        # the app from repeating error messages twice. Specifically, the item changed 
        # function is called every time a variable name is changed -- so when a user
        # inputs an invalid variable name, that is change 1 and the item changed function
        # is called. Then the function changes the variable name back to its original, valid
        # name and that is change 2 and the function is called again.
        self.already_changed = False
        self.tab1_tableWidget_VariableInfo.itemChanged.connect(self.update_variable_name)


        ###########################
        # TAB 2 UNIVARIATE TAB UI #
        ###########################

        # ADD HERE

        #######################
        # TAB 3 BIVARIATE TAB #
        #######################

        # Populate combo box for model names
        self.model_type = self.tab3_comboBox_ModelType.currentText()
        self.tab3_comboBox_ModelName.addItems(utils.LINK_MODEL_API[self.model_type].keys())

        # Activate URL for model API links
        self.model_name = self.tab3_comboBox_ModelName.currentText()
        self.url        = utils.LINK_MODEL_API[self.model_type][self.model_name]
        self.tab3_label_LinkToModelAPI.setOpenExternalLinks(True)
        self.tab3_label_LinkToModelAPI.setText(
            '''<a href='{}'>Link to Model API</a>'''.format(self.url)
            )

        # Add model parameters to plain text widget
        self.clf = utils.get_model(model_name=self.model_name, model_type=self.model_type)
        text     = utils.pretty_print_dict(self.clf.get_params())
        self.tab3_plainTextEdit_ModelParameters.setPlainText(text)

        # Connect combo box functions
        self.tab3_comboBox_ModelType.activated[str].connect(self.add_model_names)
        self.tab3_comboBox_ModelType.activated[str].connect(self.set_model_api_link)
        self.tab3_comboBox_ModelType.activated[str].connect(self.set_model_parameters)

        self.tab3_comboBox_ModelName.activated[str].connect(self.set_model_api_link)
        self.tab3_comboBox_ModelName.activated[str].connect(self.set_model_parameters)


        ################
        # VISUALIZE UI #
        ################

        # Add matplotlib widget
        self.vbox         = QVBoxLayout()
        self.MplCanvas    = DynamicMplCanvas()
        self.navi_toolbar = NavigationToolbar(self.MplCanvas, self)
        self.vbox.addWidget(self.MplCanvas)
        self.vbox.addWidget(self.navi_toolbar)
        self.vbox.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.widget_Plot.setLayout(self.vbox)

        # Connect generate button
        self.pushButton_Generate.clicked.connect(self.generate_results)

    # ~~~~~~~~~~~~~~~~~ END OF __INIT__ ~~~~~~~~~~~~~~~~~ #

    ######################
    # MENU UI: FUNCTIONS #
    ######################

    def reset(self):
        """ADD DESCRIPTION"""
        if not self.data_loaded:
            utils.message_box(message="Error With Data Reset",
                              informativeText="Reason:\nNo data loaded",
                              windowTitle="Error With Data Reset",
                              type="error") 
        else: 
            reply = QMessageBox.question(self, 
                                         'Message', 
                                         "Are you sure you want to reset the data?", 
                                         QMessageBox.Yes | QMessageBox.No, 
                                         QMessageBox.No)
            # Reset data if yes
            if reply == QMessageBox.Yes: self.load_data()


    def exit(self):
        """ADD DESCRIPTION"""
        reply = QMessageBox.question(self, 
                                     'Message', 
                                     "Are you sure you want to exit?", 
                                     QMessageBox.Yes | QMessageBox.No, 
                                     QMessageBox.No)
        # Reset data if yes
        if reply == QMessageBox.Yes: self.close()



    ###########################
    # VISUALIZE UI: FUNCTIONS #
    ###########################

    def generate_results(self):
        """ADD DESCRIPTION"""
        if self.data_loaded:
            # Information for calculations
            xlabel    = self.comboBox_XAxis.currentText()
            ylabel    = self.comboBox_YAxis.currentText()
            plot_type = self.comboBox_PlotType.currentText()

            if xlabel == 'None' and ylabel == 'None':
                utils.message_box(message="No Variables Selected for Analysis",
                                  informativeText="Select X and/or Y variable and try again",
                                  windowTitle="No Variables Selected",
                                  type="error")
                return

            # Create plot
            try:
                # Check for valid data based on plot type
                if plot_type in ['Scatter', 'Line', 'Scatter + Line']: 
                    
                    # Need X variable
                    if xlabel == 'None':
                        utils.message_box(message="Error Generating %s Plot" % plot_type,
                                          informativeText="Reason:\nNo X variable selected",
                                          windowTitle="Error Generating Plot",
                                          type="error")
                        return
                    
                    # Also need Y variable
                    if ylabel == 'None':
                        utils.message_box(message="Error Generating %s Plot" % plot_type,
                                          informativeText="Reason:\nNo Y variable selected",
                                          windowTitle="Error Generating Plot",
                                          type="error")
                        return

                # Make plot
                kwargs = {
                    'sample': self.data['Sample'],
                    'x': self.data[xlabel] if xlabel != 'None' else None,
                    'y': self.data[ylabel] if ylabel != 'None' else None,
                    'xlabel': xlabel,
                    'ylabel': ylabel,
                    'plot_type': plot_type
                    }
                Thread(target=self.MplCanvas.update_plot, kwargs=kwargs).start()

                # self.MplCanvas.update_plot(sample=self.data['Sample'],
                #                            x=self.data[xlabel] if xlabel != 'None' else None,
                #                            y=self.data[ylabel] if ylabel != 'None' else None,
                #                            xlabel=xlabel,
                #                            ylabel=ylabel,
                #                            plot_type=plot_type)
            
            # Catch plotting exception here
            except Exception as e:
                utils.message_box(message="Error Generating %s Plot" % plot_type,
                                  informativeText="Reason:\n%s" % str(e),
                                  windowTitle="Error Generating Plot",
                                  type="error")
                return

            # Calculate descriptive statistics
            try:
                self.univariate_descriptives(x=self.data[xlabel] if xlabel != 'None' else None,
                                             y=self.data[ylabel] if ylabel != 'None' else None,
                                             xlabel=xlabel,
                                             ylabel=ylabel)
            
            # Catch descriptive statistics exception here
            except Exception as e:
                utils.message_box(message="Error Calculating Univariate Statistics",
                                  informativeText="Reason:\n%s" % str(e),
                                  windowTitle="Error Calculating Statistics",
                                  type="error")
                return

        # Data not loaded yet
        else:
            utils.message_box(message="Error Generating Results",
                              informativeText="Reason:\nNo data loaded",
                              windowTitle="Error Generating Results",
                              type="error")         


    ############################
    # TAB 1 DATA UI: FUNCTIONS #
    ############################

    def update_variable_name(self):
        """ADD DESCRIPTION"""
        if self.data_loaded:

            # Find current row that was edited
            row                  = self.sender().currentRow()
            new_var_name         = \
                self.tab1_tableWidget_VariableInfo.item(row, 0).text()
            
            # If variable name not empty
            if new_var_name:

                # New variable name specified, so update names
                if new_var_name not in self.var_names:
                    # Update var_names list and update XY combo boxes
                    self.statusBar.showMessage("Changed variable %s to name %s" % (self.var_names[row], new_var_name))
                    self.var_names[row] = new_var_name
                    self.data.columns   = self.var_names
                    self.update_combobox_xyaxis()
                    self.already_changed = False

                else:
                    # Duplicate variable name passed, raise error
                    if not self.already_changed:
                        # Reset text back to original
                        self.already_changed = True
                        self.tab1_tableWidget_VariableInfo.item(row, 0).setText(self.var_names[row])
                        utils.message_box(message="Error Changing Variable Name: %s" % self.var_names[row],
                                          informativeText="Reason:\n%s name already exists" % new_var_name,
                                          windowTitle="Invalid Variable Name",
                                          type="error")
                    else:
                        self.tab1_tableWidget_VariableInfo.item(row, 0).setText(self.var_names[row])
                        self.already_changed = False


            # Empty variable name passed
            else:
                if not self.already_changed:
                    # Reset text back to original
                    self.already_changed = True
                    self.tab1_tableWidget_VariableInfo.item(row, 0).setText(self.var_names[row])
                    utils.message_box(message="Error Changing Variable Name: %s" % self.var_names[row],
                                      informativeText="Reason:\nBlank name specified",
                                      windowTitle="Invalid Variable Name",
                                      type="error")

                else:
                    self.tab1_tableWidget_VariableInfo.item(row, 0).setText(self.var_names[row])
                    self.already_changed = False


    def update_combobox_xyaxis(self):
        """ADD DESCRIPTION"""
        # Clear items first
        self.comboBox_XAxis.clear()
        self.comboBox_YAxis.clear()

        # Update items
        self.comboBox_XAxis.addItems(['None'] + self.var_names)
        self.comboBox_YAxis.addItems(['None'] + self.var_names)


    def update_variable_dtype(self):
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
            self.update_lcd_numbers()
            self.statusBar.showMessage("Converted %s to data type %s" % (var_name, new_dtype))

        except Exception as e:
            utils.message_box(message="Error Changing Data Type Data Type %s to %s" % (var_name, new_dtype),
                              informativeText="Reason:\n%s" % str(e),
                              windowTitle="Data Conversion Error",
                              type="error")

            # Set combo box back to data type before attempted conversion
            comboBox = self.tab1_tableWidget_VariableInfo.cellWidget(row, 1).findChild(QComboBox)
            comboBox.setCurrentIndex(comboBox.findText(utils.DTYPE_TO_LABEL[self.dtypes[row]], 
                                                       QtCore.Qt.MatchFixedString))
            return


    def update_lcd_numbers(self):
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


    class ThreadLoadData(QtCore.QThread):
        """ADD
        
        Parameters
        ----------
        
        Returns
        -------
        """ 
        # Define signals
        data_signal  = QtCore.Signal(list)

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
                self.data_signal.emit([data])

            except Exception as e:
                self.data_signal.emit([str(e)])


    def slot_ThreadLoadData(self, data_signal):
        """ADD
        
        Parameters
        ----------
        
        Returns
        -------
        """
        # Unpack signal
        signal = data_signal[0]

        # Check instance and update GUI
        if isinstance(signal, pd.DataFrame):
            self.tab1_tableWidget_VariableInfo.setRowCount(0)

            # Get data, map dtypes to string, and add rows to table
            self.data      = signal
            self.dtypes    = map(str, self.data.dtypes)
            self.var_names = self.data.columns.tolist()
            for var_name, dtype in zip(self.var_names, self.dtypes):
                self.add_data_row(var_name, dtype)

            # Update lcd displays and combo boxes for plotting
            self.tab1_lcdNumber_Rows.display(self.data.shape[0])
            self.tab1_lcdNumber_Columns.display(self.data.shape[1])
            self.update_lcd_numbers()
            self.update_combobox_xyaxis()
            self.statusBar.showMessage("Data loaded with %d rows and %d columns" % \
                                        (self.data.shape))
            self.data_loaded = True

        else:
            utils.message_box(message="Error Loading Data File %s" % self.file,
                              informativeText="Reason:\n%s" % signal,
                              windowTitle="I/O Error",
                              type="error")
        

    def load_data(self):
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
            self.data_loaded = False
            self.file        = file # Define as attribute for accessing in other functions
            self.data_thread = self.ThreadLoadData(file)
            self.data_thread.data_signal.connect(self.slot_ThreadLoadData)
            self.data_thread.start()


    def add_data_row(self, var_name, dtype):
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
            combo_box.currentIndexChanged.connect(self.update_variable_dtype)

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


    ##################################
    # TAB 2 UNIVARIATE UI: FUNCTIONS #
    ##################################


    class ThreadUnivariateDescriptives(QtCore.QThread):
        """ADD
        
        Parameters
        ----------
        
        Returns
        -------
        """
        # Define signals
        data_signal = QtCore.Signal(list)

        def __init__(self, x, y, xlabel, ylabel):
            QtCore.QThread.__init__(self)
            self.x      = x
            self.y      = y
            self.xlabel = xlabel
            self.ylabel = ylabel

        def __del__(self):
            """ADD DESCRIPTION"""
            self.wait()

        def run(self):
            """ADD DESCRIPTION"""
            try:
                # X variable
                if self.xlabel != 'None':
                    x_stats   = utils.univariate_statistics(self.x)
                    x_freq    = pd.value_counts(self.x)
                    x_numeric = utils.is_numeric(self.x)
                    if x_numeric: x_freq = utils.value_counts_grouped(self.x, x_freq)
                else:
                    x_stats   = pd.DataFrame([])
                    x_freq    = pd.DataFrame([])
                    x_numeric = 0 

                # Y variable
                if self.ylabel != 'None':
                    y_stats   = utils.univariate_statistics(self.y)
                    y_freq    = pd.value_counts(self.y)
                    y_numeric = utils.is_numeric(self.y)
                    if y_numeric: y_freq = utils.value_counts_grouped(self.y, y_freq)
                else:
                    y_stats   = pd.DataFrame([])
                    y_freq    = pd.DataFrame([])
                    y_numeric = 0 

                # Success signal
                self.data_signal.emit(['Success', x_stats, y_stats, x_freq, 
                                         y_freq, x_numeric, y_numeric, self.xlabel, 
                                         self.ylabel])

            except Exception as e:
                # Error signal
                self.data_signal.emit([str(e), x_stats, y_stats, x_freq, 
                                         y_freq,x_numeric, y_numeric, self.xlabel, 
                                         self.ylabel])


    def slot_ThreadUnivariateDescriptives(self, data_signal):
        """ADD
        
        Parameters
        ----------
        
        Returns
        -------
        """
        # Unpack signal information
        status    = data_signal[0]
        x_stats   = data_signal[1]
        y_stats   = data_signal[2]
        x_freq    = data_signal[3]
        y_freq    = data_signal[4]
        x_numeric = data_signal[5]
        y_numeric = data_signal[6]
        xlabel    = data_signal[7]
        ylabel    = data_signal[8]

        # Clear tables
        self.tab2_tableWidget_Xstats.setRowCount(0)
        self.tab2_tableWidget_Xfreq.setRowCount(0)
        self.tab2_tableWidget_Ystats.setRowCount(0)
        self.tab2_tableWidget_Yfreq.setRowCount(0)

        # Update GUI
        if status != 'Success':
            utils.message_box(message="Error Generating Univariate Statistics",
                              informativeText="Reason:\n%s" % status,
                              windowTitle="Calculation Error",
                              type="error")
        else:
            # X variable
            if xlabel != 'None':
                # Calculate descriptives and populate table
                for key, value in x_stats.iteritems():

                    # Insert row
                    idx = self.tab2_tableWidget_Xstats.rowCount()
                    self.tab2_tableWidget_Xstats.insertRow(idx)

                    # Create table items and make sure not editable
                    name_item = QTableWidgetItem(key)
                    name_item.setFlags(QtCore.Qt.ItemIsEnabled)

                    key_item  = QTableWidgetItem('%.3f' % value)
                    key_item.setFlags(QtCore.Qt.ItemIsEnabled)
                    key_item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

                    # Insert items into table
                    self.tab2_tableWidget_Xstats.setItem(idx, 0, name_item)
                    self.tab2_tableWidget_Xstats.setItem(idx, 1, key_item)

                # Test if x is numeric, then create grouped frequency table
                for i in xrange(x_freq.shape[0]):

                    # Insert row
                    idx = self.tab2_tableWidget_Xfreq.rowCount()
                    self.tab2_tableWidget_Xfreq.insertRow(idx)

                    # Create table items and make sure not editable
                    if x_numeric:
                        name_item = QTableWidgetItem(x_freq.index[i])
                        key_item  = QTableWidgetItem('%d' % x_freq.values[i][0])
                    else:
                        name_item = QTableWidgetItem('%.3f' % x_freq.index[i])
                        key_item  = QTableWidgetItem('%d' % x_freq.values[i])

                    name_item.setFlags(QtCore.Qt.ItemIsEnabled)
                    key_item.setFlags(QtCore.Qt.ItemIsEnabled)
                    key_item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

                    # Insert items into table
                    self.tab2_tableWidget_Xfreq.setItem(idx, 0, name_item)
                    self.tab2_tableWidget_Xfreq.setItem(idx, 1, key_item)

            # Y variable
            if ylabel != 'None':
                # Calculate descriptives and populate table
                for key, value in y_stats.iteritems():

                    # Insert row
                    idx = self.tab2_tableWidget_Ystats.rowCount()
                    self.tab2_tableWidget_Ystats.insertRow(idx)

                    # Create table items and make sure not editable
                    name_item = QTableWidgetItem(key)
                    name_item.setFlags(QtCore.Qt.ItemIsEnabled)

                    key_item  = QTableWidgetItem('%.3f' % value)
                    key_item.setFlags(QtCore.Qt.ItemIsEnabled)
                    key_item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

                    # Insert items into table
                    self.tab2_tableWidget_Ystats.setItem(idx, 0, name_item)
                    self.tab2_tableWidget_Ystats.setItem(idx, 1, key_item)

                # Calculate frequencies and populate table
                for i in xrange(y_freq.shape[0]):

                    # Insert row
                    idx = self.tab2_tableWidget_Yfreq.rowCount()
                    self.tab2_tableWidget_Yfreq.insertRow(idx)

                    # Create table items and make sure not editable
                    if y_numeric:
                        name_item = QTableWidgetItem(y_freq.index[i])
                        key_item  = QTableWidgetItem('%d' % y_freq.values[i][0])

                    else:
                        name_item = QTableWidgetItem('%.3f' % y_freq.index[i])
                        key_item  = QTableWidgetItem('%d' % y_freq.values[i])

                    name_item.setFlags(QtCore.Qt.ItemIsEnabled)
                    key_item.setFlags(QtCore.Qt.ItemIsEnabled)
                    key_item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

                    # Insert items into table
                    self.tab2_tableWidget_Yfreq.setItem(idx, 0, name_item)
                    self.tab2_tableWidget_Yfreq.setItem(idx, 1, key_item)


    def univariate_descriptives(self, x, y, xlabel, ylabel):
        """ADD
        
        Parameters
        ----------
        
        Returns
        -------
        """
        self.univariate_thread = \
                self.ThreadUnivariateDescriptives(x=x, y=y, xlabel=xlabel, ylabel=ylabel)
        self.univariate_thread.data_signal.connect(self.slot_ThreadUnivariateDescriptives)        
        self.univariate_thread.start()


    #################################
    # TAB 3 BIVARIATE UI: FUNCTIONS #
    #################################

    def add_model_names(self):
        """ADD DESCRIPTION"""
        self.model_type = self.tab3_comboBox_ModelType.currentText()
        self.tab3_comboBox_ModelName.clear()
        self.tab3_comboBox_ModelName.addItems(utils.LINK_MODEL_API[self.model_type].keys())


    def set_model_api_link(self):
        """ADD DESCRIPTION"""
        self.model_type = self.tab3_comboBox_ModelType.currentText()
        self.model_name = self.tab3_comboBox_ModelName.currentText()
        self.url = utils.LINK_MODEL_API[self.model_type][self.model_name]
        self.tab3_label_LinkToModelAPI.setText(
            '''<a href='{}'>Link to Model API</a>'''.format(self.url)
            )

    def set_model_parameters(self):
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