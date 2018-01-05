# -*- coding: utf-8 -*-

# Import libraries from api
from main_api import *


class EDAViewer(QMainWindow):
    """Main window for exploratory data analysis viewer"""
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        # General setup and connect menu, tabs, and visualize interfaces
        self.setup_general()
        self.setup_menu_ui()
        self.setup_data_ui()        
        self.setup_univariate_ui()
        self.setup_bivariate_ui()
        self.setup_visualize_ui()

    # ~~~~~~~~~~~~~~~~~ END OF __INIT__ ~~~~~~~~~~~~~~~~~ #

    ###################
    # MISC: FUNCTIONS #
    ###################

    def setup_general(self):
        """ADD DESCRIPTION"""
        # Load .ui file dynamically for now
        utils.load_ui(utils.UI_PATH, self)

        # Set window title and icon, status bar, and force tab widget to open on data tab
        self.setWindowTitle('Exploratory Data Analysis Viewer')
        self.setWindowIcon(QIcon(os.path.join(utils.ICONS_PATH, 'chart-line_black.png')))
        self.statusBar.showMessage("""Click "Load Data" button to begin""")
        self.tabWidget_Analysis.setCurrentIndex(0)


    ######################
    # MENU UI: FUNCTIONS #
    ######################

    def setup_menu_ui(self):
        """Initialize menu items interface"""

        # File -> Reset data button
        self.menuItem_ResetData.triggered.connect(self.reset)
        self.menuItem_ResetData.setIcon(QIcon(os.path.join(utils.ICONS_PATH, 'refresh.png')))

        # File -> Save -> Data button
        self.menuItem_Data.triggered.connect(self.save_data)
        self.menuItem_Data.setIcon(QIcon(os.path.join(utils.ICONS_PATH, 'database.png')))

        # File -> Save -> Statistics button
        self.menuItem_Statistics.triggered.connect(self.save_statistics)
        self.menuItem_Statistics.setIcon(QIcon(os.path.join(utils.ICONS_PATH, 'chart-timeline.png')))

        # File -> Save -> Plot button
        self.menuItem_Plot.triggered.connect(self.save_plot)
        self.menuItem_Plot.setIcon(QIcon(os.path.join(utils.ICONS_PATH, 'image-area.png')))

        # File -> Save
        self.menuItem_Save.setIcon(QIcon(os.path.join(utils.ICONS_PATH, 'content-save.png')))

        # File -> Save -> Save All button
        self.menuItem_All.triggered.connect(self.save_all)
        self.menuItem_All.setIcon(QIcon(os.path.join(utils.ICONS_PATH, 'content-save-all.png')))

        # File -> Exit button
        self.menuItem_Exit.triggered.connect(self.exit)
        self.menuItem_Exit.setIcon(QIcon(os.path.join(utils.ICONS_PATH, 'window-close.png')))

        # Help -> Documentation button
        self.menuItem_Documentation.triggered.connect(self.show_documentation)
        self.menuItem_Documentation.setIcon(QIcon(os.path.join(utils.ICONS_PATH, 'application.png')))

        # Help -> About button
        self.menuItem_About.triggered.connect(AboutUi)
        self.menuItem_About.setIcon(QIcon(os.path.join(utils.ICONS_PATH, 'information-outline.png')))


    class ThreadSaveData(QtCore.QThread):
        """ADD
        
        Parameters
        ----------
        
        Returns
        -------
        """ 
        # Define signals
        data_signal = QtCore.Signal(list)

        def __init__(self, data, filename):
            QtCore.QThread.__init__(self)
            self.data     = data
            self.filename = filename

        def __del__(self):
            """ADD DESCRIPTION"""
            self.wait()

        def run(self):
            """ADD DESCRIPTION"""
            try:
                self.data.to_csv(self.filename, index=False)
                self.data_signal.emit(['Success'])
            except Exception as e:
                self.data_signal.emit([str(e)])


    def slot_ThreadSaveData(self, data_signal):
        """ADD
        
        Parameters
        ----------
        
        Returns
        -------
        """
        # Unpack signal and check status
        status = data_signal[0]
        if status != 'Success':
            utils.message_box(message="Error Saving Data",
                              informativeText="Reason:\n%s" % status,
                              type="error")

    def save_data(self):
        """Saves data as specified extension"""
        if self.data_loaded:
            try:
                options   = QFileDialog.Options()
                options   |= QFileDialog.DontUseNativeDialog
                file_info = QFileDialog.getSaveFileName(self, "Save Data", "/",
                                                        "*.csv;;"
                                                        "*.tsv;;"
                                                        "*.txt",
                                                        options=options)
                if file_info[0]: 
                    filename = ''.join(''.join(file_info).split('*'))
                    self.save_data_thread = self.ThreadSaveData(data=self.data,
                                                                filename=filename)
                    self.save_data_thread.data_signal.connect(self.slot_ThreadSaveData)
                    self.save_data_thread.start()
            
            except Exception as e:
                utils.message_box(message="Error Saving Data",
                                  informativeText="Reason:\n%s" % str(e),
                                  type="error")         

        else:
            utils.message_box(message="Error Saving Data",
                              informativeText="Reason:\nNo data loaded",
                              type="error")


    def reset(self):
        """Resets data to original names and data types"""
        if not self.data_loaded:
            utils.message_box(message="Error With Data Reset",
                              informativeText="Reason:\nNo data loaded",
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
        """Exits application"""
        reply = QMessageBox.question(self, 
                                     'Message', 
                                     "Are you sure you want to exit?", 
                                     QMessageBox.Yes | QMessageBox.No, 
                                     QMessageBox.No)
        # Reset data if yes
        if reply == QMessageBox.Yes: self.close()        


    def save_statistics(self):
        """Saves x and/or y variable statistics and frequency tables"""
        # TODO: threading

        # Check to make sure stats are first generated
        if self.stats_generated['status']:
            save_directory = QFileDialog.getExistingDirectory(self, 
                                                             "Select directory to save statistics", 
                                                             "/")
            if save_directory:
                try:
                    data   = {}
                    xlabel = self.stats_generated['xlabel']
                    ylabel = self.stats_generated['ylabel']
                    
                    # Add x variable
                    if xlabel != 'None':
                        data[xlabel + '_stats'] = self.tab2_tableWidget_Xstats
                        data[xlabel + '_freq']  = self.tab2_tableWidget_Xfreq
                    
                    # Add y variable
                    if ylabel != 'None':
                        data[ylabel + '_stats'] = self.tab2_tableWidget_Ystats
                        data[ylabel + '_freq']  = self.tab2_tableWidget_Yfreq
                    
                    # Convert table widgets to pandas dataframes and write to disk
                    dfs = utils.tablewidgets_to_dataframes(data)
                    for basename, df in dfs.iteritems():
                        fullname = os.path.join(save_directory, basename + '.csv')
                        df.to_csv(fullname)

                except Exception as e:
                    utils.message_box(message="Error Saving Statistics",
                                      informativeText="Reason:\n%s" % str(e),
                                      type="error") 

        else:
            utils.message_box(message="Error Saving Statistics",
                              informativeText="Reason:\nNo statistics calculated",
                              type="error")         


    def save_plot(self):
        """Saves current generated plot"""
        if self.plot_generated['status']:
            try:
                options   = QFileDialog.Options()
                options   |= QFileDialog.DontUseNativeDialog
                file_info = QFileDialog.getSaveFileName(self, "Save Plot", 
                                                        "/", "*.png", options=options)
                if file_info[0]: self.MplCanvas.fig.savefig(file_info[0] + '.png', dpi=150)

            except Exception as e:
                utils.message_box(message="Error Saving Plot",
                                  informativeText="Reason:\n%s" % str(e),
                                  type="error")         

        else:
            utils.message_box(message="Error Saving Plot",
                              informativeText="Reason:\nNo plot generated",
                              type="error")         


    def save_all(self):
        """Saves data, statistics, and plot"""
        try:
            self.save_data()
            self.save_statistics()
            self.save_plot()

        except Exception as e:
            utils.message_box(message="Error Saving All",
                              informativeText="Reason:\n%s" % str(e),
                              type="error")         


    def show_documentation(self):
        """Shows documentation for application"""
        utils.message_box(message="Documentation Not Currently Available",
                          informativeText="",
                          type="warning")         
        return 



    ###########################
    # VISUALIZE UI: FUNCTIONS #
    ###########################

    def setup_visualize_ui(self):
        """ADD DESCRIPTION"""
        # Add matplotlib widget
        self.plot_generated = {'status': False, 'xlabel': 'None', 'ylabel': 'None'}
        self.vbox           = QVBoxLayout()
        self.MplCanvas      = DynamicMplCanvas()
        self.navi_toolbar   = NavigationToolbar(self.MplCanvas, self)
        self.vbox.addWidget(self.MplCanvas)
        self.vbox.addWidget(self.navi_toolbar)
        self.vbox.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.widget_Plot.setLayout(self.vbox)

        # Connect generate button
        self.pushButton_Generate.clicked.connect(self.generate_results)
        self.pushButton_Generate.setIcon(QIcon(os.path.join(utils.ICONS_PATH, 'play.png')))

        # Connect combo boxes to check boxes
        self.comboBox_XAxis.activated.connect(self.update_checkbox)
        self.comboBox_YAxis.activated.connect(self.update_checkbox)
        self.checkBox_StandardizeX.setEnabled(False)
        self.checkBox_StandardizeY.setEnabled(False)


    def update_combobox_xyaxis(self):
        """ADD DESCRIPTION"""
        # Clear items first
        self.comboBox_XAxis.clear()
        self.comboBox_YAxis.clear()

        # Update items
        self.comboBox_XAxis.addItems(['None'] + self.var_names)
        self.comboBox_YAxis.addItems(['None'] + self.var_names)


    def update_checkbox(self):
        """ADD DESCRIPTION"""
        xlabel = self.comboBox_XAxis.currentText()
        ylabel = self.comboBox_YAxis.currentText()

        if xlabel == 'None':
            self.checkBox_StandardizeX.setEnabled(False)
        else:
            if not utils.is_numeric(self.data[xlabel]):
                self.checkBox_StandardizeX.setEnabled(False)
            else:
                self.checkBox_StandardizeX.setEnabled(True)

        if ylabel == 'None': 
            self.checkBox_StandardizeY.setEnabled(False)
        else:
            if not utils.is_numeric(self.data[ylabel]):
                self.checkBox_StandardizeY.setEnabled(False)
            else:
                self.checkBox_StandardizeY.setEnabled(True)


    class ThreadUpdatePlot(QtCore.QThread):
        """ADD
        
        Parameters
        ----------
        
        Returns
        -------
        """ 
        # Define signals
        data_signal = QtCore.Signal(list)

        def __init__(self, pushButton, func, kwargs):
            QtCore.QThread.__init__(self)
            self.func   = func
            self.kwargs = kwargs

            # Change status of push button
            pushButton.setText('Running') 
            pushButton.setStyleSheet('background-color:green;') 
            pushButton.setIcon(QIcon(os.path.join(utils.ICONS_PATH, 'run.png')))
            pushButton.setDisabled(True)

        def __del__(self):
            """ADD DESCRIPTION"""
            self.wait()

        def run(self):
            """ADD DESCRIPTION"""
            status = self.func(**self.kwargs)
            self.data_signal.emit([status])


    def slot_ThreadUpdatePlot(self, data_signal):
        """ADD
        
        Parameters
        ----------
        
        Returns
        -------
        """
        # Unpack signal and check status
        status = data_signal[0]
        if status != 'Success':
            utils.message_box(message="Error Generating Plot",
                              informativeText="Reason:\n%s" % status,
                              type="error")


    def update_plot(self, pushButton, func, kwargs):
        """ADD
        
        Parameters
        ----------
        
        Returns
        -------
        """
        self.update_plot_thread = \
                self.ThreadUpdatePlot(pushButton=pushButton, func=func, kwargs=kwargs)
        self.update_plot_thread.data_signal.connect(self.slot_ThreadUpdatePlot)        
        self.update_plot_thread.start()



    def generate_results(self):
        """ADD DESCRIPTION"""
        if self.data_loaded:
            # Information for calculations
            xlabel    = self.comboBox_XAxis.currentText()
            ylabel    = self.comboBox_YAxis.currentText()
            plot_type = self.comboBox_PlotType.currentText()

            # No labels specified
            if xlabel == 'None' and ylabel == 'None':
                utils.message_box(message="No Variables Selected for Analysis",
                                  informativeText="Select X and/or Y variable and try again",
                                  type="error")
                return

            # Check for valid data based on plot type
            if plot_type in ['Scatter', 'Line', 'Scatter + Line']: 
                
                # Need X variable
                if xlabel == 'None':
                    utils.message_box(message="Error Generating %s Plot" % plot_type,
                                      informativeText="Reason:\nNo X variable selected",
                                      type="error")
                    return
                
                # Also need Y variable
                if ylabel == 'None':
                    utils.message_box(message="Error Generating %s Plot" % plot_type,
                                      informativeText="Reason:\nNo Y variable selected",
                                      type="error")
                    return

            # Select x and y variables and standardize if specified
            x = self.data[xlabel] if xlabel != 'None' else None
            if self.checkBox_StandardizeX.isEnabled() and self.checkBox_StandardizeX.isChecked():
                x = (x - x.mean())/x.std()

            y = self.data[ylabel] if ylabel != 'None' else None
            if self.checkBox_StandardizeY.isEnabled() and self.checkBox_StandardizeY.isChecked():
                y = (y - y.mean())/y.std()

            # Update plot (in separate thread)
            kwargs = {
                'x': x,
                'y': y,
                'xlabel': xlabel,
                'ylabel': ylabel,
                'plot_type': plot_type,
                'plot_generated': self.plot_generated, # Thread will set this flag to True when done
                'checkbox': self.tab3_checkBox_AddPredictions
                }
            self.update_plot(pushButton=self.pushButton_Generate, func=self.MplCanvas.update_plot, 
                             kwargs=kwargs)

            # Calculate descriptive statistics (in separate thread)
            self.univariate_descriptives(x=x,
                                         y=y,
                                         xlabel=xlabel,
                                         ylabel=ylabel)

            # Reset models fitted info
            self.tab3_plainTextEdit_ModelSummary.clear()
            self._n_models_fitted = 0


        # Data not loaded yet
        else:
            utils.message_box(message="Error Generating Results",
                              informativeText="Reason:\nNo data loaded",
                              type="error")         
            return


    ############################
    # TAB 1 DATA UI: FUNCTIONS #
    ############################

    def setup_data_ui(self):
        """ADD DESCRIPTION"""
        # Connect load data button
        self.data_loaded = False
        self.tab1_tableWidget_VariableInfo.horizontalHeader().setVisible(True)
        self.tab1_pushButton_LoadData.clicked.connect(self.load_data)
        self.tab1_pushButton_LoadData.setIcon(QIcon(os.path.join(utils.ICONS_PATH, 'play.png')))

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
                                      type="error")

                else:
                    self.tab1_tableWidget_VariableInfo.item(row, 0).setText(self.var_names[row])
                    self.already_changed = False


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
            self.update_checkbox()
            self.statusBar.showMessage("Converted %s to data type %s" % (var_name, new_dtype))

        except Exception as e:
            utils.message_box(message="Error Changing Data Type Data Type %s to %s" % (var_name, new_dtype),
                              informativeText="Reason:\n%s" % str(e),
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
        data_signal = QtCore.Signal(list)

        def __init__(self, file, pushButton):
            QtCore.QThread.__init__(self)
            self.file = file

            # Change button to running status
            pushButton.setText('Running') 
            pushButton.setStyleSheet('background-color:green;') 
            pushButton.setIcon(QIcon(os.path.join(utils.ICONS_PATH, 'run.png')))
            pushButton.setDisabled(True)

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

            # Change back button
            self.tab1_pushButton_LoadData.setText('Data Loaded') 
            self.tab1_pushButton_LoadData.setStyleSheet('') 
            self.tab1_pushButton_LoadData.setIcon(QIcon(os.path.join(utils.ICONS_PATH, 'play.png')))
            self.tab1_pushButton_LoadData.setDisabled(True)

        else:
            utils.message_box(message="Error Loading Data File %s" % self.file,
                              informativeText="Reason:\n%s" % signal,
                              type="error")

            # Change back button
            self.tab1_pushButton_LoadData.setText('Load Data') 
            self.tab1_pushButton_LoadData.setStyleSheet('') 
            self.tab1_pushButton_LoadData.setIcon(QIcon(os.path.join(utils.ICONS_PATH, 'play.png')))
            self.tab1_pushButton_LoadData.setDisabled(False)


    def load_data(self):
        """ADD DESCRIPTION"""
        if not self.data_loaded:
            # File dialog options for opening single file
            options   = QFileDialog.Options()
            options   |= QFileDialog.DontUseNativeDialog
            file_info = QFileDialog.getOpenFileName(self, "Load Data", "/",
                                                    "*.csv files (*.csv);;"
                                                    "*.tsv files (*tsv);;"
                                                    "*.txt files (*.txt);;",
                                                    options=options)

            # If a file is selected, try and open
            if file_info[0]:
                self.data_loaded = False
                self.file        = file_info[0] # Define as attribute for accessing in other functions
                self.data_thread = self.ThreadLoadData(self.file, self.tab1_pushButton_LoadData)
                self.data_thread.data_signal.connect(self.slot_ThreadLoadData)
                self.data_thread.start()
        
        # Try data reset here
        else:
            try:
                # Create new thread for resetting data
                self.data_loaded       = False
                self.reset_data_thread = self.ThreadLoadData(self.file, self.tab1_pushButton_LoadData)
                self.reset_data_thread.data_signal.connect(self.slot_ThreadLoadData)
                self.reset_data_thread.start()

                # Reset plot
                self.MplCanvas.update_plot(x=[1, 2, 3], 
                                           y=[1, 1, 1], 
                                           xlabel='X', 
                                           ylabel='Y',
                                           plot_type='Line',
                                           plot_generated={'status': False, 'xlabel': None, 'ylabel': None},
                                           checkbox=QCheckBox)
                self.plot_generated = {'status': False, 'xlabel': 'None', 'ylabel': 'None'}

                # Reset univariate results
                self.tab2_tableWidget_Xstats.setRowCount(0)
                self.tab2_tableWidget_Xfreq.setRowCount(0)
                self.tab2_tableWidget_Ystats.setRowCount(0)
                self.tab2_tableWidget_Yfreq.setRowCount(0)
                self.stats_generated = {'status': False, 'xlabel': 'None', 'ylabel': 'None'}

                # Reset bivariate results
                self.tab3_plainTextEdit_ModelSummary.clear()
                self.tab3_plainTextEdit_ModelSummary.clear()
                self.set_model_parameters()

            except Exception as e:
                utils.message_box(message="Error Resetting Data",
                                  informativeText="Reason:\n%s\n\nTIP: Try restarting application" % str(e),
                                  type="error")


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
            fixed_item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            fixed_item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.tab1_tableWidget_VariableInfo.setItem(idx, 1, fixed_item)


    ##################################
    # TAB 2 UNIVARIATE UI: FUNCTIONS #
    ##################################

    def setup_univariate_ui(self):
        """ADD DESCRIPTION"""
        # Data structure about stats generated
        self.stats_generated = {'status': False, 'xlabel': 'None', 'ylabel': 'None'}

        # Enable add headers for table widgets
        self.tab2_tableWidget_Xstats.horizontalHeader().setVisible(True)
        self.tab2_tableWidget_Ystats.horizontalHeader().setVisible(True)
        self.tab2_tableWidget_Xfreq.horizontalHeader().setVisible(True)
        self.tab2_tableWidget_Yfreq.horizontalHeader().setVisible(True)

        # Setup size of each column
        self.tab2_tableWidget_Xstats.horizontalHeader().setResizeMode(0, QHeaderView.Stretch)
        self.tab2_tableWidget_Xstats.horizontalHeader().setResizeMode(1, QHeaderView.ResizeToContents)
        self.tab2_tableWidget_Ystats.horizontalHeader().setResizeMode(0, QHeaderView.Stretch)
        self.tab2_tableWidget_Ystats.horizontalHeader().setResizeMode(1, QHeaderView.ResizeToContents)
        self.tab2_tableWidget_Xfreq.horizontalHeader().setResizeMode(0, QHeaderView.Stretch)
        self.tab2_tableWidget_Xfreq.horizontalHeader().setResizeMode(1, QHeaderView.ResizeToContents)
        self.tab2_tableWidget_Yfreq.horizontalHeader().setResizeMode(0, QHeaderView.Stretch)
        self.tab2_tableWidget_Yfreq.horizontalHeader().setResizeMode(1, QHeaderView.ResizeToContents)

        # Update labels to reflect currently selected variable
        self.tab2_label_XVariable.setText('X-Variable: %s' % self.comboBox_XAxis.currentText())
        self.tab2_label_YVariable.setText('Y-Variable: %s' % self.comboBox_YAxis.currentText())



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
                    x_stats   = None
                    x_freq    = None
                    x_numeric = None

                # Y variable
                if self.ylabel != 'None':
                    y_stats   = utils.univariate_statistics(self.y)
                    y_freq    = pd.value_counts(self.y)
                    y_numeric = utils.is_numeric(self.y)
                    if y_numeric: y_freq = utils.value_counts_grouped(self.y, y_freq)
                else:
                    y_stats   = None
                    y_freq    = None
                    y_numeric = None

                # Success signal
                self.data_signal.emit(['Success', x_stats, y_stats, x_freq, 
                                        y_freq, x_numeric, y_numeric, self.xlabel, 
                                        self.ylabel])

            except Exception as e:
                # Error signal
                self.data_signal.emit([str(e)])


    def slot_ThreadUnivariateDescriptives(self, data_signal):
        """ADD
        
        Parameters
        ----------
        
        Returns
        -------
        """
        status = data_signal[0]

        # Update GUI
        if status != 'Success':
            utils.message_box(message="Error Generating Univariate Statistics",
                              informativeText="Reason:\n%s" % status,
                              type="error")

        else:
            # Unpack remainder of signal information
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

            # Update labels to reflect current variables selected
            self.tab2_label_XVariable.setText('X-Variable: %s' % self.comboBox_XAxis.currentText())
            self.tab2_label_YVariable.setText('Y-Variable: %s' % self.comboBox_YAxis.currentText())
            
            # X variable
            if xlabel != 'None':
                # Calculate descriptives and populate table
                for key, value in x_stats.iteritems():
                    try:
                        # Insert row
                        idx = self.tab2_tableWidget_Xstats.rowCount()
                        self.tab2_tableWidget_Xstats.insertRow(idx)

                        # Create table items and make sure not editable
                        name_item = QTableWidgetItem(key)
                        name_item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                        name_item.setFlags(QtCore.Qt.ItemIsEnabled)

                        key_item  = QTableWidgetItem('%.3f' % value)
                        key_item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                        key_item.setFlags(QtCore.Qt.ItemIsEnabled)

                        # Insert items into table
                        self.tab2_tableWidget_Xstats.setItem(idx, 0, name_item)
                        self.tab2_tableWidget_Xstats.setItem(idx, 1, key_item)
                    except:
                        continue

                # Test if x is numeric, then create grouped frequency table
                for i in xrange(x_freq.shape[0]):
                    try:
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
                        name_item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                        key_item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

                        # Insert items into table
                        self.tab2_tableWidget_Xfreq.setItem(idx, 0, name_item)
                        self.tab2_tableWidget_Xfreq.setItem(idx, 1, key_item)
                    except:
                        continue

            # Y variable
            if ylabel != 'None':
                # Calculate descriptives and populate table
                for key, value in y_stats.iteritems():
                    try:
                        # Insert row
                        idx = self.tab2_tableWidget_Ystats.rowCount()
                        self.tab2_tableWidget_Ystats.insertRow(idx)

                        # Create table items and make sure not editable
                        name_item = QTableWidgetItem(key)
                        name_item.setFlags(QtCore.Qt.ItemIsEnabled)
                        name_item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

                        key_item  = QTableWidgetItem('%.3f' % value)
                        key_item.setFlags(QtCore.Qt.ItemIsEnabled)
                        key_item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

                        # Insert items into table
                        self.tab2_tableWidget_Ystats.setItem(idx, 0, name_item)
                        self.tab2_tableWidget_Ystats.setItem(idx, 1, key_item)
                    except:
                        continue

                # Calculate frequencies and populate table
                for i in xrange(y_freq.shape[0]):
                    try:
                        # Insert row
                        idx = self.tab2_tableWidget_Yfreq.rowCount()
                        self.tab2_tableWidget_Yfreq.insertRow(idx)

                        # Create table items and make sure not editable
                        name_item = QTableWidgetItem(str(y_freq.index[i]))
                        if y_numeric:
                            key_item  = QTableWidgetItem('%d' % y_freq.values[i][0])
                        else:
                            key_item  = QTableWidgetItem('%d' % y_freq.values[i])

                        name_item.setFlags(QtCore.Qt.ItemIsEnabled)
                        key_item.setFlags(QtCore.Qt.ItemIsEnabled)
                        name_item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                        key_item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

                        # Insert items into table
                        self.tab2_tableWidget_Yfreq.setItem(idx, 0, name_item)
                        self.tab2_tableWidget_Yfreq.setItem(idx, 1, key_item)

                    except:
                        continue

            # Update status of stats generated variables
            self.stats_generated['status'] = True
            self.stats_generated['xlabel'] = xlabel
            self.stats_generated['ylabel'] = ylabel

        # Set back original push button
        self.pushButton_Generate.setText('Generate') 
        self.pushButton_Generate.setStyleSheet('') 
        self.pushButton_Generate.setIcon(QIcon(os.path.join(utils.ICONS_PATH, 'play.png')))
        self.pushButton_Generate.setDisabled(False)


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

    def setup_bivariate_ui(self):
        """ADD DESCRIPTION"""
        # Populate combo box for model names
        self._n_models_fitted = 0
        self.model_type       = self.tab3_comboBox_ModelType.currentText()
        self.tab3_comboBox_ModelName.addItems(utils.LINK_MODEL_API[self.model_type].keys())

        # Activate URL for model API links
        self.model_name = self.tab3_comboBox_ModelName.currentText()
        self.url        = utils.LINK_MODEL_API[self.model_type][self.model_name]
        self.tab3_label_LinkToModelAPI.setOpenExternalLinks(True)
        self.tab3_label_LinkToModelAPI.setText(
            '''<a href='{}'>Link to Model API</a>'''.format(self.url)
            )

        # Add model parameters to plain text widget
        model = utils.get_model(model_name=self.model_name, model_type=self.model_type)
        text  = utils.pretty_print_dict(model.get_params())
        self.tab3_plainTextEdit_ModelParameters.setPlainText(text)

        # Connect Clear button
        self.tab3_pushButton_Clear.clicked.connect(self.tab3_plainTextEdit_ModelSummary.clear)
        self.tab3_pushButton_Clear.setIcon(QIcon(os.path.join(utils.ICONS_PATH, 'eraser.png')))

        # Connect combo box functions
        self.tab3_comboBox_ModelType.activated[str].connect(self.add_model_names)
        self.tab3_comboBox_ModelType.activated[str].connect(self.set_model_api_link)
        self.tab3_comboBox_ModelType.activated[str].connect(self.set_model_parameters)

        self.tab3_comboBox_ModelName.activated[str].connect(self.set_model_api_link)
        self.tab3_comboBox_ModelName.activated[str].connect(self.set_model_parameters)

        # Connect fit model button
        self.tab3_pushButton_FitModel.clicked.connect(self.fit_model)
        self.tab3_pushButton_FitModel.setIcon(QIcon(os.path.join(utils.ICONS_PATH, 'play.png')))

        # Disable add predictions checkbox for now
        self.tab3_checkBox_AddPredictions.setEnabled(False)


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
        clf  = utils.get_model(model_name=self.model_name, model_type=self.model_type)
        text = utils.pretty_print_dict(clf.get_params())
        self.tab3_plainTextEdit_ModelParameters.setPlainText(text)


    class ThreadFitModel(QtCore.QThread):
        """ADD
        
        Parameters
        ----------
        
        Returns
        -------
        """ 
        # Define signals
        data_signal  = QtCore.Signal(list)

        def __init__(self, X, y, xlabel, ylabel, model_type, model, pushButton):
            QtCore.QThread.__init__(self)

            # Define attributes
            self.X          = X
            self.y          = y
            self.xlabel     = xlabel
            self.ylabel     = ylabel
            self.model_type = model_type
            self.model      = model

            # Change button to running status
            pushButton.setText('Running') 
            pushButton.setStyleSheet('background-color:green;') 
            pushButton.setIcon(QIcon(os.path.join(utils.ICONS_PATH, 'run.png')))
            pushButton.setDisabled(True)

        def __del__(self):
            """ADD DESCRIPTION"""
            self.wait()

        def run(self):
            """ADD DESCRIPTION"""
            try:
                # Clustering model
                if self.model_type == 'Clustering':
                    X_             = np.column_stack([self.X, self.y.reshape(-1, 1)])
                    y_pred, scores = utils.unsupervised_ml(X=X_, model=self.model)

                # Regression or classification model
                else:
                    y_pred, scores = \
                    utils.supervised_ml(X=self.X, y=self.y, model=self.model, 
                        model_type=self.model_type)

                # Emit all signals
                self.data_signal.emit(['Success', y_pred, scores, self.xlabel, self.ylabel])

            except Exception as e:
                self.data_signal.emit([str(e)])


    def slot_ThreadFitModel(self, data_signal):
        """ADD
        
        Parameters
        ----------
        
        Returns
        -------
        """
        status = data_signal[0]
        if status != 'Success':
            utils.message_box(message="Error Fitting Model",
                              informativeText="Reason:\n%s" % status,
                              type="error") 
        else:
            # Unpack results and update widget
            self._n_models_fitted += 1
            y_pred = data_signal[1]
            scores = data_signal[2] 
            xlabel = data_signal[3]
            ylabel = data_signal[4]

            # Clear widget and write overall model information
            self.tab3_plainTextEdit_ModelSummary.insertPlainText("Model ID: %d\nModel Type: %s\nModel Name: %s\n\n" % \
                    ((self._n_models_fitted), self.model_type, self.model_name))

            self.tab3_plainTextEdit_ModelSummary.insertPlainText("X-Axis: %s\nY-Axis: %s\n\n"  % \
                    (xlabel, ylabel))

            # Write specific model information to widget
            if self.model_type in ['Classification', 'Regression']: 
                if self.model_type == 'Classification': 
                    metric_str = 'Accuracy'
                else:
                    metric_str = 'Mean Squared Error'

                # CV results
                for fold, score in enumerate(scores):
                    self.tab3_plainTextEdit_ModelSummary.insertPlainText("Fold %d: %s = %.3f\n" % \
                        ((fold+1), metric_str, score))

                self.tab3_plainTextEdit_ModelSummary.insertPlainText("Overall %s: %.3f +/- %.3f\n" % \
                        (metric_str, scores.mean(), scores.std()))
                self.tab3_plainTextEdit_ModelSummary.insertPlainText('--------\n\n')

            else:
                metric_str = ['Silhouette Score', 'Calinski Harabaz Score']

                # Write specific model information to widget
                for name, metric in zip(metric_str, scores):
                    self.tab3_plainTextEdit_ModelSummary.insertPlainText("Metric: %s = %.3f\n" % \
                        (name, metric))  
                self.tab3_plainTextEdit_ModelSummary.insertPlainText('--------\n\n')


        # If add predictions to plot
        if self.tab3_checkBox_AddPredictions.isChecked():
            self.add_predictions(y_pred=y_pred, xlabel=xlabel, ylabel=ylabel, 
                                 model_type=self.model_type, model_name=self.model_name)

        # Change back to original push button
        self.tab3_pushButton_FitModel.setText('Fit Model') 
        self.tab3_pushButton_FitModel.setStyleSheet('') 
        self.tab3_pushButton_FitModel.setIcon(QIcon(os.path.join(utils.ICONS_PATH, 'play.png')))
        self.tab3_pushButton_FitModel.setDisabled(False)


    def run(self, X, y, xlabel, ylabel, model):
        """ADD
        
        Parameters
        ----------
        
        Returns
        -------
        """
        self.fit_model_thread = \
            self.ThreadFitModel(X=X, y=y, xlabel=xlabel, ylabel=ylabel, model_type=self.model_type, 
                                model=model, pushButton=self.tab3_pushButton_FitModel)
        self.fit_model_thread.data_signal.connect(self.slot_ThreadFitModel)
        self.fit_model_thread.start()


    def fit_model(self):
        """ADD
        
        Parameters
        ----------
        
        Returns
        -------
        """
        if self.data_loaded:
            # Grab labels and plot type
            xlabel    = self.comboBox_XAxis.currentText()
            ylabel    = self.comboBox_YAxis.currentText()
            plot_type = self.comboBox_PlotType.currentText()

            # Both variables need to be specified
            if xlabel == 'None' and ylabel == 'None':
                utils.message_box(message="Error Fitting %s Model" % self.model_type,
                                  informativeText="Reason:\nX and Y variable not specified",
                                  type="error")
                return

            # If add predictions to plot checked, check for valid plot
            if self.tab3_checkBox_AddPredictions.isChecked():
                if plot_type not in utils.PLOTS_FOR_PRED:
                    utils.message_box(message="Unable to Adding Predictions to %s Plot" % plot_type,
                                      informativeText="Reason:\n%s plot is not a valid plot to add predictions" % plot_type,
                                      type="error")
                    return

                # If add predictions to plot checked, make sure plot is already generated
                if not self.plot_generated['status']:
                    utils.message_box(message="Error Adding Predictions to %s Plot" % plot_type,
                                      informativeText="Reason:\nNo plot generated yet",
                                      type="error")
                    return

            # Try and convert x and y to numeric for machine learning model
            try:
                X = self.data[xlabel].values.astype(float).reshape(-1, 1)
                y = self.data[ylabel].values.astype(float)
            
            except Exception as e:
                utils.message_box(message="Error Fitting %s Model" % self.model_type,
                                  informativeText="Reason:\n%s" % str(e),
                                  type="error")
                return

            # Ensure label is categorical (based on CV splits) prior to fitting classifier
            if self.model_type == 'Classification' and not utils.check_for_categorical_label(y):
                utils.message_box(message="Error Fitting %s Model" % self.model_type,
                                  informativeText="Reason:\nLess than 3 samples per unique value",
                                  type="error")
                return       

            # Try and convert hyperparameter text to dictionary and instantiate model
            try:
                params = utils.text_to_dict(self.tab3_plainTextEdit_ModelParameters.toPlainText())
                model  = utils.get_model(model_name=self.model_name, model_type=self.model_type)

                # Now try and update model with each parameter and skip ones that are invalid
                n_failed, n_names = 0, []
                for key, value in params.iteritems():
                    try:
                        model.set_params(**{key: value})
                    except:
                        n_failed += 1
                        n_names.append({key: value})
                        pass

                if n_failed > 0:
                    utils.message_box(message="Error Setting %d Model Parameters for %s Model" % self.model_name,
                                      informativeText="Parameters:\n%s" % (n_names,),
                                      type="warning")

            except Exception as e:
                utils.message_box(message="Error Loading Parameters for %s Model" % self.model_name,
                                  informativeText="Reason:\n%s" % str(e),
                                  type="error")
                return

            # Run model (in separate thread)  
            self.run(X=X, y=y, xlabel=xlabel, ylabel=ylabel, model=model)

        else:
            utils.message_box(message="Error Fitting %s Model" % self.model_type,
                              informativeText="Reason:\nNot data loaded",
                              type="error")
            return 


    class ThreadAddPredictionsToPlot(QtCore.QThread):
        """ADD
        
        Parameters
        ----------
        
        Returns
        -------
        """ 
        # Define signals
        data_signal = QtCore.Signal(list)

        def __init__(self, func, kwargs):
            QtCore.QThread.__init__(self)
            self.func   = func
            self.kwargs = kwargs

        def __del__(self):
            """ADD DESCRIPTION"""
            self.wait()

        def run(self):
            """ADD DESCRIPTION"""
            status = self.func(**self.kwargs)
            self.data_signal.emit([status]) 


    def slot_ThreadAddPredictionsToPlot(self, data_signal):
        """ADD
        
        Parameters
        ----------
        
        Returns
        -------
        """
        status = data_signal[0]
        if status != 'Success':
            utils.message_box(message="Error Adding Predictions to Plot",
                              informativeText="Reason:\n%s" % status,
                              type="error")   


    def add_predictions(self, y_pred, xlabel, ylabel, model_type, model_name):
        """ADD
        
        Parameters
        ----------
        
        Returns
        -------
        """
        # Warning if plot variables are not same as machine learning variables
        if xlabel != self.plot_generated['xlabel'] or ylabel != self.plot_generated['ylabel']:
            reply = utils.message_box(message="Warning Variable Mismatch",
                                    informativeText=("Machine learning variables do not match plot "
                                                     "variables. Do you want to add predictions?"),
                                    type="warning",
                                    question=True) 
            
            if reply == QMessageBox.No: return

        # Create thread and add predictions
        self.add_prediction_thread = \
            self.ThreadAddPredictionsToPlot(func=self.MplCanvas.add_predictions_to_plot,
                                            kwargs={'y_pred': y_pred,
                                                    'model_type': model_type,
                                                    'model_name': model_name})
        self.add_prediction_thread.data_signal.connect(self.slot_ThreadAddPredictionsToPlot)        
        self.add_prediction_thread.start()


if __name__ == "__main__":
    # Create main thread
    app = QApplication(sys.argv)

    # Set window icon and application name
    app.setWindowIcon(QIcon(os.path.join(utils.ICONS_PATH, 'app_icon.png')))
    app.setApplicationName("Exploratory Data Analysis Viewer")
    app.setStyleSheet(qdarkstyle.load_stylesheet())

    # Initialize EDAViewer
    window = EDAViewer()
    window.showMaximized()
    sys.exit(app.exec_())