import os
from shutil import copy
from pathlib import Path
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon
from qgis.utils import iface
from qgis.core import QgsApplication, QgsProject, QgsExpressionContextUtils, QgsSettings
from .setup_dialog import SetupDialog
from .source_dialog import SourceDialog

edit_icon = QIcon(':/qt-project.org/qtgradienteditor/images/edit.png')
info_icon = QIcon(':/qt-project.org/styles/commonstyle/images/fileinfo-16.png')

class ProjectSetupPlugin:
    def __init__(self, iface):
        super().__init__()
        project = QgsProject.instance()
        self.iface = iface
        self.home_path = os.path.expanduser('~')
        if QgsExpressionContextUtils.globalScope().variable('gpkg_path'):
            self.gpkg_path = QgsExpressionContextUtils.globalScope().variable('gpkg_path')
        else:
            self.gpkg_path = os.path.expanduser('~')

    def initGui(self):
        self.menu = iface.pluginMenu().addMenu('Project Setup')
        self.menu.setObjectName('project_setup_menu')

        self.setupAction = QAction(edit_icon, "Project Setup...")
        self.iface.addPluginToMenu("Project Setup", self.setupAction)
        self.setupAction.triggered.connect(self.projectSetup)

        self.sourceAction = QAction(info_icon, "Add Project Datasource...")
        self.iface.addPluginToMenu("Project Setup", self.sourceAction)
        self.sourceAction.triggered.connect(self.projectSources)

    #TODO this doesn't work correctly
    def unload(self):
        self.iface.removePluginMenu('Project Setup', self.setupAction)
        self.iface.removePluginMenu('Project Setup', self.sourceAction)
        menubar = self.menu.parentWidget()
        menubar.removeAction(self.menu.menuAction())

    def projectSetup(self):
        dialog = SetupDialog(self.gpkg_path, self.home_path)
        dialog.exec()
        if dialog.success == True:
            self.getValues(dialog)
            self.setVariables()
           
    def projectSources(self):
        dialog = SourceDialog(self.gpkg_path, self.home_path)
        dialog.exec()
        if dialog.success == True:
            self.getValues(dialog)
            self.setVariables()

    def getValues(self, dialog):
        self.filename = dialog.filename
        self.proj_num = dialog.proj_num
        self.proj_name = dialog.proj_name
        self.client = dialog.client
        self.loc = dialog.loc
        self.sources = dialog.sources
        self.gpkg_location = dialog.gpkg_location
        self.gpkg_templates = dialog.gpkg_templates

    def setVariables(self):
        project = QgsProject.instance()
        if self.filename:
            self.filename = project.writePath(self.filename)
            project.write(self.filename)       
            iface.mainWindow().setWindowTitle(QgsExpressionContextUtils.projectScope(project).variable('project_filename'))
        if self.gpkg_templates:
            pass
        if self.proj_num:
            QgsExpressionContextUtils.setProjectVariable(project, 'project_identifier', self.proj_num)
        if self.proj_name:
            QgsExpressionContextUtils.setProjectVariable(project, 'project_title', self.proj_name)
        if self.client:
            QgsExpressionContextUtils.setProjectVariable(project, 'project_client', self.client)
        if self.loc:
            QgsExpressionContextUtils.setProjectVariable(project, 'project_location', self.loc)
        if self.sources:
            if QgsExpressionContextUtils.projectScope(project).variable('Project Data Sources'):
                new_sources = []
                for item in QgsExpressionContextUtils.projectScope(project).variable('project_sources'):
                    new_sources.append(item)
                for item in self.sources:
                    if item not in new_sources:
                        new_sources.append(item)
                QgsExpressionContextUtils.setProjectVariable(project, 'Project Data Sources', new_sources)
            else:
                QgsExpressionContextUtils.setProjectVariable(project, 'Project Data Sources', self.sources)

    def copyTemplates(self):
        for template in self.gpkg_templates:
            basename = os.path.basename(template)
            filename = os.path.join(self.gpkg_location, basename)
            copy(template, filename)
            # s = QgsSettings()
            # use QgsAbstractDatabaseProviderConnection to establish the connection
            # use QgsSettings.setValue to add the connection to settings
            # s.value('providers/ogr/GPKG/connections/Template.gpkg/path') = path_to_gpkg
            iface.mainWindow().findChildren(QWidget, 'Browser')[0].refresh()
            # add list of connections to project variables
            # on project load, remove old connections, add correct ones
