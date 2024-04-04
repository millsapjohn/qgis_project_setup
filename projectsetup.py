from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon
from qgis.utils import iface
from qgis.core import QgsApplication, QgsProject, QgsExpressionContextUtils
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
        self.setVariables()
           
    def projectSources(self):
        dialog = SourceDialog()
        dialog.exec()
        self.getValues(dialog)
        self.setVariables()

    def getValues(self, dialog):
        self.proj_num = dialog.proj_num
        self.proj_name = dialog.proj_name
        self.client = dialog.client
        self.loc = dialog.loc
        self.sources = dialog.sources

    def setVariables(self):
        project = QgsProject.instance()
        if self.proj_num:
            QgsExpressionContextUtils.setProjectVariable(project, 'project number', self.proj_num)
        if self.proj_name:
            QgsExpressionContextUtils.setProjectVariable(project, 'Project Name', self.proj_name)
        if self.client:
            QgsExpressionContextUtils.setProjectVariable(project, 'Project Client', self.client)
        if self.loc:
            QgsExpressionContextUtils.setProjectVariable(project, 'Project Location', self.loc)
        if self.sources:
            if QgsExpressionContextUtils.projectScope(project).variable('Project Data Sources'):
                new_sources = []
                for item in QgsExpressionContextUtils.projectScope(project).variable('Project Data Sources'):
                    new_sources.append(item)
                for item in self.sources:
                    if item not in new_sources:
                        new_sources.append(item)
                QgsExpressionContextUtils.setProjectVariable(project, 'Project Data Sources', new_sources)
            else:
                QgsExpressionContextUtils.setProjectVariable(project, 'Project Data Sources', self.sources)
