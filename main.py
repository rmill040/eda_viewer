from __future__ import division, print_function

from PySide import QtCore
from PySide.QtGui import QApplication, QMainWindow
import qdarkstyle
import sys

# Custom functions
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



        #############################
        # CONNECT UNIVARIATE TAB UI #
        #############################



        #########################
        # CONNECT BIVARIATE TAB #
        #########################



        ########################
        # CONNECT VISUALIZE UI #
        ########################



if __name__ == "__main__":
    app = QApplication(sys.argv)
    if utils.USE_DARK_THEME: app.setStyleSheet(qdarkstyle.load_stylesheet())
    window = Ui()
    window.showMaximized()
    sys.exit(app.exec_())