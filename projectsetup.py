from PyQt5.QtWidgets import QAction, QMessageBox, QWidget, QVBoxLayout, QDialog, QLineEdit, QPushButton
from PyQt5.QtGui import QIcon
from qgis.utils import iface
from qgis.core import QgsApplication, QgsProject
from .setup_dialog import SetupDialog
from .source_dialog import SourceDialog

edit_icon = QIcon(':/qt-project.org/qtgradienteditor/images/edit.png')
info_icon = QIcon(':/qt-project.org/styles/commonstyle/images/fileinfo-16.png')

class ProjectSetupPlugin:
    def __init__(self, iface):
        super().__init__()
        project = QgsProject.instance()
        self.iface = iface

    def initGui(self):
        self.menu = iface.pluginMenu().addMenu('Project Setup')
        self.menu.setObjectName('project_setup_menu')

        self.setupAction = QAction(edit_icon, "Project Setup...")
        self.iface.addPluginToMenu("Project Setup", self.setupAction)
        self.setupAction.triggered.connect(self.projectSetup)

        self.sourceAction = QAction(info_icon, "Add Project Datasource...")
        self.iface.addPluginToMenu("Project Setup", self.sourceAction)
        self.sourceAction.triggered.connect(self.projectSources)

    def unload(self):
        self.iface.removePluginMenu('Project Setup', self.setupAction)
        self.iface.removePluginMenu('Project Setup', self.sourceAction)
        menubar = self.menu.parentWidget()
        menubar.removeAction(self.menu.menuAction())

    def projectSetup(self):
        dialog = SetupDialog()
        dialog.exec()
        self.getValues(dialog)
        for source in self.sources:
            iface.messageBar().pushMessage(source)
           
    def projectSources(self):
        dialog = SourceDialog()
        dialog.exec()
        self.getValues(dialog)

    def getValues(self, dialog):
        self.proj_num = dialog.proj_num
        self.proj_name = dialog.proj_name
        self.client = dialog.client
        self.loc = dialog.loc
        self.sources = dialog.sources

    def setVariables(self):
        pass
