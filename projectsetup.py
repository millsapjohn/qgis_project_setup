from PyQt5.QtWidgets import QAction, QMessageBox, QWidget
from PyQt5.QtGui import QIcon
from qgis.utils import iface
from qgis.core import QgsApplication, QgsProject

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
        self.setupAction.triggered.connect(self.showSetup)

        self.sourceAction = QAction(info_icon, "Add Project Datasource...")
        self.iface.addPluginToMenu("Project Setup", self.sourceAction)
        self.sourceAction.triggered.connect(self.showSources)

    def unload(self):
        self.iface.removePluginMenu('Project Setup', self.setupAction)
        self.iface.removePluginMenu('Project Setup', self.sourceAction)
        menubar = self.menu.parentWidget()
        menubar.removeAction(self.menu.menuAction())

    def showSetup(self):
        self.iface.messageBar().pushMessage('Project Setup')
        mb = QMessageBox()
        mb.setText('Project Setup')
        mb.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        return_val = mb.exec()
        if return_val == QMessageBox.Ok:
            self.iface.messageBar().pushMessage('Ok')
        elif return_val == QMessageBox.Cancel:
            self.iface.messageBar().pushMessage('Cancel')

    def showSources(self):
        self.iface.messageBar().pushMessage('Edit Sources')
