from qgis.utils import iface
from .setup_dialog import SetupDialog

class SourceDialog(SetupDialog):
    def __init__(self):
        super().__init__()
        self.iface = iface
        self.updateUI()

    def updateUI(self):
        self.setWindowTitle('Add/Remove Data Sources')
        self.hide_widgets()
