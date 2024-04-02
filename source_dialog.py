from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QListWidget, QHBoxLayout
from PyQt5.QtGui import QIcon
from qgis.utils import iface
from .setup_dialog import SetupDialog

class SourceDialog(SetupDialog):
    def __init__(self):
        super().__init__()
        self.iface = iface
        self.updateUI()

    def updateUI(self):
        self.setWindowTitle('Add/Remove Data Sources')
        self.proj_num_box.hide()
        self.proj_num_label.hide()
        self.proj_name_box.hide()
        self.proj_name_label.hide()
        self.client_label.hide()
        self.client_box.hide()
        self.loc_label.hide()
        self.loc_box.hide()
