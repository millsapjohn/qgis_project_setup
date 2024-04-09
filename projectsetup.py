import os
from shutil import copy
from pathlib import Path
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon
from qgis.utils import iface
from qgis.core import QgsApplication, QgsProject, QgsExpressionContextUtils, QgsProviderRegistry, QgsVectorLayer
from osgeo import ogr
from .setup_dialog import SetupDialog
from .source_dialog import SourceDialog
from .connection_dialog import ConnectionDialog

edit_icon = QIcon(':/qt-project.org/qtgradienteditor/images/edit.png')
info_icon = QIcon(':/qt-project.org/styles/commonstyle/images/fileinfo-16.png')
connect_icon = QIcon(':/images/themes/default/mIconConnect.svg')
file_icon = QIcon(':/images/themes/default/mActionFileSave.svg')

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
        self.setupAction = QAction(edit_icon, "Project Setup...")
        self.iface.addPluginToMenu("Manage Project", self.setupAction)
        self.setupAction.triggered.connect(self.projectSetup)

        self.sourceAction = QAction(info_icon, "Manage Project Datasources...")
        self.iface.addPluginToMenu("Manage Project", self.sourceAction)
        self.sourceAction.triggered.connect(self.projectSources)

        self.connectionAction = QAction(connect_icon, 'Manage Persistent GeoPackage Connections...')
        self.iface.addPluginToMenu("Manage Project", self.connectionAction)
        self.connectionAction.triggered.connect(self.projectConnections)

    def unload(self):
        self.iface.removePluginMenu('Manage Project', self.setupAction)
        self.iface.removePluginMenu('Manage Project', self.sourceAction)
        self.iface.removePluginMenu('Manage Project', self.connectionAction)
        del self.setupAction
        del self.sourceAction
        del self.connectionAction

    def projectSetup(self):
        project = QgsProject.instance()
        if QgsExpressionContextUtils.projectScope(project).variable('project_sources'):
            curr_sources = QgsExpressionContextUtils.projectScope(project).variable('project_sources').split(";")
        else:
            curr_sources = []
        dialog = SetupDialog(self.gpkg_path, self.home_path, curr_sources)
        dialog.exec()
        if dialog.success == True:
            if not dialog.filename:
                iface.messageBar().pushMessage('No filename specified')
            elif dialog.gpkg_templates and not dialog.gpkg_location:
                iface.messageBar().pushMessage('No GeoPackage save location specified')
            else:
                self.getValues(dialog)
                self.setVariables()
                QgsProject.instance().write()
           
    def projectSources(self):
        project = QgsProject.instance()
        if QgsExpressionContextUtils.projectScope(project).variable('project_sources'):
            curr_sources = QgsExpressionContextUtils.projectScope(project).variable('project_sources').split(";")
        else:
            curr_sources = []
        dialog = SourceDialog(self.gpkg_path, self.home_path, curr_sources)
        dialog.exec()
        if dialog.success == True:
            self.getSources(dialog)
            self.setSources()
            project.write()

    def projectConnections(self):
        md = QgsProviderRegistry.instance().providerMetadata('ogr')
        curr_conn = []
        for item in md.connections():
            curr_conn.append(item)
        dialog = ConnectionDialog(curr_conn)
        dialog.exec()
        if dialog.success == True:
            self.getConnections(dialog)

    def getConnections(self, dialog):
        project = QgsProject.instance()
        if dialog.gpkg_connections:
            self.gpkg_connections = dialog.gpkg_connections
        else:
            pass
        if not QgsExpressionContextUtils.projectScope(project).variable('project_gpkg_connections'):
            QgsExpressionContextUtils.projectScope(project).setVariable('project_gpkg_connections', self.gpkg_connections)
        else:
            conn_str = QgsExpressionContextUtils.projectScope(project).variable('project_gpkg_connections')
            conn_str.append(self.gpkg_connections)
            QgsExpressionContextUtils.projectScope(project).setVariable('project_gpkg_connections', conn_str)

    def getValues(self, dialog):
        if dialog.filename:
            self.filename = dialog.filename
        if dialog.proj_num:
            self.proj_num = dialog.proj_num
        if dialog.proj_name:
            self.proj_name = dialog.proj_name
        if dialog.client:
            self.client = dialog.client
        if dialog.loc:
            self.loc = dialog.loc
        if dialog.sources:
            self.sources = dialog.sources
        if dialog.gpkg_location:
            self.gpkg_location = dialog.gpkg_location
        if dialog.gpkg_templates:
            self.gpkg_templates = dialog.gpkg_templates

    def getSources(self, dialog):
        if dialog.sources:
            self.sources = dialog.sources

    def setVariables(self):
        project = QgsProject.instance()
        if self.filename:
            self.filename = project.writePath(self.filename)
            project.write(self.filename)       
            iface.mainWindow().setWindowTitle(QgsExpressionContextUtils.projectScope(project).variable('project_filename'))
        project = QgsProject().instance()
        if self.gpkg_templates:
            self.copyTemplates()
            QgsExpressionContextUtils.setProjectVariable(project, 'project_gpkg_connections', self.gpkg_connections)
        if self.proj_num:
            QgsExpressionContextUtils.setProjectVariable(project, 'project_number', self.proj_num)
        if self.proj_name:
            QgsExpressionContextUtils.setProjectVariable(project, 'project_name', self.proj_name)
        if self.client:
            QgsExpressionContextUtils.setProjectVariable(project, 'project_client', self.client)
        if self.loc:
            QgsExpressionContextUtils.setProjectVariable(project, 'project_location', self.loc)
        if self.sources:
                QgsExpressionContextUtils.setProjectVariable(project, 'project_sources', self.sources)
        project.write()

    def setSources(self):
        project = QgsProject.instance()
        if self.sources:
            QgsExpressionContextUtils.setProjectVariable(project, 'project_sources', self.sources)

    def copyTemplates(self):
        self.gpkg_connections = ""
        md = QgsProviderRegistry.instance().providerMetadata('ogr')
        for template in self.gpkg_templates:
            basename = os.path.basename(template)
            if self.proj_num:
                basename = self.proj_num + "_" + basename
            filename = os.path.join(self.gpkg_location, basename)
            copy(template, filename)
            layer = [l.GetName() for l in ogr.Open(filename)][0]
            layer_path = filename + "|layername={layer}"
            vl = QgsVectorLayer(layer_path, basename, 'ogr')
            conn = md.createConnection(vl.dataProvider().dataSourceUri(), {})
            md.saveConnection(conn, basename)
            self.gpkg_connections = self.gpkg_connections + basename + ";" + filename + ";"
        iface.reloadConnections()
