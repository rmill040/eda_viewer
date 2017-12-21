from __future__ import division, print_function

from PySide.QtUiTools import QUiLoader
from PySide.QtCore import QFile, QMetaObject

###############
"""CONSTANTS"""
###############

UI_PATH        = '/Users/R2/Documents/EDAViewer/gui.ui'
USE_DARK_THEME = True


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