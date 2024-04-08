from qgis.utils import iface
from .setup_dialog import SetupDialog

class ConnectionDialog(SetupDialog):
    def __init__(self, gpkg_path, home_path):
        self.gpkg_path = gpkg_path
        self.home_path = home_path
        super().__init__(self.gpkg_path, self.home_path)
        self.iface = iface
        self.updateUI()

    # inherits from the SetupDialog class and removes unnecessary elements. Inheritance the other way wasn't working.
    def updateUI(self):
        self.setWindowTitle('Add/Remove Data Sources')
        self.hide_source_widgets()