# -*- coding: utf-8 -*-

# Import libraries from api
from about_api import *


class AboutUi(object):
    """ADD

    Parameters
    ----------
    
    Returns
    -------
    """
    def __init__(self):
        # Define QDialog as modal application window
        self.dialog = QDialog()
        self.dialog.setObjectName("Dialog")
        self.dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        self.dialog.setModal(True)

        # Set window title
        self.dialog.setWindowTitle("About")

        # Define grid for layout
        self.gridLayout = QGridLayout(self.dialog)
        self.gridLayout.setObjectName("gridLayout")

        ## label
        self.label_author = QLabel(self.dialog)
        self.label_author.setAlignment(QtCore.Qt.AlignRight)
        self.label_author.setText("Author:")
        self.gridLayout.addWidget(self.label_author, 0, 0, 1, 1)

        ## input
        self.input_author = QLabel(self.dialog)
        self.input_author.setAlignment(QtCore.Qt.AlignLeft)
        self.input_author.setText(utils.AUTHOR)
        self.gridLayout.addWidget(self.input_author, 0, 1, 1, 1)

        ## label
        self.label_version = QLabel(self.dialog)
        self.label_version.setAlignment(QtCore.Qt.AlignRight)
        self.label_version.setText("Version:")
        self.gridLayout.addWidget(self.label_version, 1, 0, 1, 1)

        ## input
        self.input_version = QLabel(self.dialog)
        self.input_version.setAlignment(QtCore.Qt.AlignLeft)
        self.input_version.setText(utils.VERSION)
        self.gridLayout.addWidget(self.input_version, 1, 1, 1, 1)

        ## label
        self.label_builtwith = QLabel(self.dialog)
        self.label_builtwith.setAlignment(QtCore.Qt.AlignRight)
        self.label_builtwith.setText("Built With:")
        self.gridLayout.addWidget(self.label_builtwith, 2, 0, 1, 1)

        ## input
        self.input_builtwith = QLabel(self.dialog)
        self.input_builtwith.setAlignment(QtCore.Qt.AlignLeft)
        self.input_builtwith.setText(utils.BUILT_WITH)
        self.gridLayout.addWidget(self.input_builtwith, 2, 1, 1, 1)

        ## label
        self.label_website = QLabel(self.dialog)
        self.label_website.setAlignment(QtCore.Qt.AlignRight)
        self.label_website.setText("Website:")
        self.gridLayout.addWidget(self.label_website, 3, 0, 1, 1)

        ## input
        self.input_website = QLabel(self.dialog)
        self.input_website.setAlignment(QtCore.Qt.AlignLeft)
        self.input_website.setText(
            '''<a href='{}'>{}</a>'''.format(utils.WEBSITE, utils.WEBSITE)
            )
        self.input_website.setOpenExternalLinks(True)
        self.gridLayout.addWidget(self.input_website, 3, 1, 1, 1)

        ## label
        self.label_license = QLabel(self.dialog)
        self.label_license.setAlignment(QtCore.Qt.AlignRight)
        self.label_license.setText("License:")
        self.gridLayout.addWidget(self.label_license, 4, 0, 1, 1)

        ## input
        self.input_license = QLabel(self.dialog)
        self.input_license.setAlignment(QtCore.Qt.AlignLeft)
        self.input_license.setText(
            '''<a href='{}'>MIT</a>'''.format(utils.LICENSE)
            )
        self.input_license.setOpenExternalLinks(True)
        self.gridLayout.addWidget(self.input_license, 4, 1, 1, 1)

        # Spacer for adding space between hyperparameters and save button
        self.spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.okButton = QPushButton(self.dialog)
        self.okButton.setText("OK")

        # Add spacer and ok button
        self.gridLayout.addItem(self.spacer, 5, 1, 1, 1)
        self.gridLayout.addWidget(self.okButton, 6, 0, 1, 3, QtCore.Qt.AlignHCenter)
        self.okButton.clicked.connect(self.dialog.close)

        # Show QDialog
        self.dialog.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    window = AboutUi()
    sys.exit(app.exec_())