from qgis.utils import iface
from .setup_dialog import SetupDialog

class SourceDialog(SetupDialog):
    def __init__(self, gpkg_path, home_path):
        self.gpkg_path = gpkg_path
        self.home_path = home_path
        super().__init__(self.gpkg_path, self.home_path)
        self.iface = iface
        self.updateUI()

    def updateUI(self):
        self.setWindowTitle('Add/Remove Data Sources')
        self.hide_widgets()
