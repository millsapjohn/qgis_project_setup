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
            if not hasattr(dialog, 'filename'):
                iface.messageBar().pushMessage('No filename specified')
            elif hasattr(dialog, 'gpkg_templates') and not hasattr(dialog, 'gpkg_location'):
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
        project = QgsProject.instance()
        md = QgsProviderRegistry.instance().providerMetadata('ogr')
        self.curr_conn = []
        self.saved_conn = []
        if QgsExpressionContextUtils.projectScope(project).variable('project_gpkg_connections'):
            saved_conn_raw = QgsExpressionContextUtils.projectScope(project).variable('project_gpkg_connections').split(";")
            self.saved_conn = saved_conn_raw[0::2] # get every other item in the list
            self.saved_conn = [x for x in self.saved_conn if x]
        for item in md.connections():
            if item not in self.saved_conn:
                self.curr_conn.append(item)
        dialog = ConnectionDialog(self.curr_conn, self.saved_conn)
        dialog.exec()
        if dialog.success == True:
            self.getConnections(dialog)
            self.setConnections()
            project.write()

    def getConnections(self, dialog):
        project = QgsProject.instance()
        md = QgsProviderRegistry.instance().providerMetadata('ogr')
        self.conn_str = ""
        if dialog.gpkg_connections != []:
            self.gpkg_connections = dialog.gpkg_connections
            for item in self.gpkg_connections:
                conn = md.connections()[item]
                path = conn.uri()
                self.conn_str = self.conn_str + item + ";" + path + ";"

    def setConnections(self):
        project = QgsProject.instance()
        if self.conn_str:
            QgsExpressionContextUtils.setProjectVariable(project, 'project_gpkg_connections', self.conn_str)

    def getValues(self, dialog):
        if hasattr(dialog, 'filename'):
            self.filename = dialog.filename
        else:
            self.filename = ""
        if hasattr(dialog, 'proj_num'):
            self.proj_num = dialog.proj_num
        else:
            self.proj_num = ""
        if hasattr(dialog, 'proj_name'):
            self.proj_name = dialog.proj_name
        else:
            self.proj_name = ""
        if hasattr(dialog, 'client'):
            self.client = dialog.client
        else: self.client = ""
        if hasattr(dialog, 'loc'):
            self.loc = dialog.loc
        else:
            self.loc = dialog.loc
        if hasattr(dialog, 'addr'):
            self.addr = dialog.addr
        else:
            self.addr = ""
        if hasattr(dialog, 'sources'):
            self.sources = dialog.sources
        else:
            self.sources = ""
        if hasattr(dialog, 'des_by'):
            self.des_by = dialog.des_by
        else:
            self.des_by = ""
        if hasattr(dialog, 'rev_by'):
            self.rev_by = dialog.rev_by
        else:
            self.rev_by = ""
        if hasattr(dialog, 'gpkg_location'):
            self.gpkg_location = dialog.gpkg_location
        else:
            self.gpkg_location = ""
        if hasattr(dialog, 'gpkg_templates'):
            self.gpkg_templates = dialog.gpkg_templates
        else:
            self.gpkg_templates = ""

    def getSources(self, dialog):
        if hasattr(dialog, 'sources'):
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
        if self.addr:
            QgsExpressionContextUtils.setProjectVariable(project, 'project_address', self.addr)
        if self.des_by:
            QgsExpressionContextUtils.setProjectVariable(project, 'designed_by', self.des_by)
        if self.rev_by:
            QgsExpressionContextUtils.setProjectVariable(project, 'reviewed_by', self.rev_by)
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
            if basename == "Blank.gpkg":
                if self.proj_num:
                    basename = f"{self.proj_num}.gpkg"
                else:
                    basename = "_.gpkg"
            else:
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
