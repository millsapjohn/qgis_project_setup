from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QListWidget, QHBoxLayout, QFileDialog, QCheckBox
from PyQt5.QtGui import QIcon
from qgis.utils import iface


class SetupDialog(QDialog):
    def __init__(self, gpkg_path, home_path, curr_sources):
        super().__init__()
        self.iface = iface
        self.gpkg_path = gpkg_path
        self.home_path = home_path
        self.curr_sources = curr_sources
        self.success = False
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Project Setup')
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # save file location UI elements
        self.proj_file_loc_label = QLabel('Project Save Location: ')
        self.layout.addWidget(self.proj_file_loc_label)
        self.file_layout = QHBoxLayout()
        self.file_box = QLineEdit('Save File Location: ')
        self.file_layout.addWidget(self.file_box)
        self.file_button = QPushButton(text='...')
        self.file_button.clicked.connect(self.getSaveFile)
        self.file_layout.addWidget(self.file_button)
        self.layout.addLayout(self.file_layout)

        # checkbox to control other geopackage UI elements
        self.gpkg_template_checkbox = QCheckBox('Import Template GeoPackages?')
        self.layout.addWidget(self.gpkg_template_checkbox)
        self.gpkg_template_checkbox.stateChanged.connect(self.setGpkgVisibility)

        # set overall gpkg layout, will contain other sub layouts
        self.gpkg_layout = QVBoxLayout()
        # template section of the gpkg layout should be horizontal
        self.gpkg_template_layout = QHBoxLayout()
        self.gpkg_template_label = QLabel('GeoPackage Template(s): ')
        self.gpkg_template_layout.addWidget(self.gpkg_template_label)
        self.gpkg_template_location_box = QLineEdit('GeoPackage Template(s): ')
        self.gpkg_template_layout.addWidget(self.gpkg_template_location_box)
        self.gpkg_template_location_box.setDisabled(True)
        self.gpkg_template_button = QPushButton(text='...')
        self.gpkg_template_button.clicked.connect(self.getGpkgTemplates)
        self.gpkg_template_layout.addWidget(self.gpkg_template_button)
        self.gpkg_template_button.setDisabled(True)
        self.gpkg_layout.addLayout(self.gpkg_template_layout)
        # save location section of the gpkg layout
        self.gpkg_save_layout = QHBoxLayout()
        self.gpkg_location_label = QLabel('GeoPackage Save Location: ')
        self.gpkg_save_layout.addWidget(self.gpkg_location_label)
        self.gpkg_location_box = QLineEdit('GeoPackage Save Location: ')
        self.gpkg_save_layout.addWidget(self.gpkg_location_box)
        self.gpkg_location_box.setDisabled(True)
        self.gpkg_location_button = QPushButton(text='...')
        self.gpkg_location_button.clicked.connect(self.getGpkgLocation)
        self.gpkg_save_layout.addWidget(self.gpkg_location_button)
        self.gpkg_location_button.setDisabled(True)
        self.gpkg_layout.addLayout(self.gpkg_save_layout)
        self.layout.addLayout(self.gpkg_layout)

        # project number UI elements
        self.proj_num_label = QLabel('Project Number: ')
        self.layout.addWidget(self.proj_num_label)
        self.proj_num_box = QLineEdit()
        self.layout.addWidget(self.proj_num_box)

        # project name UI elements
        self.proj_name_label = QLabel('Project Name: ')
        self.layout.addWidget(self.proj_name_label)
        self.proj_name_box = QLineEdit()
        self.layout.addWidget(self.proj_name_box)

        # project client UI elements
        self.client_label = QLabel('Client: ')
        self.layout.addWidget(self.client_label)
        self.client_box = QLineEdit()
        self.layout.addWidget(self.client_box)

        # project location UI elements
        self.loc_label = QLabel('Project Location: ')
        self.layout.addWidget(self.loc_label)
        self.loc_box = QLineEdit()
        self.layout.addWidget(self.loc_box)

        # data sources UI elements
        self.source_label = QLabel('Data Sources: ')
        self.layout.addWidget(self.source_label)
        self.source_list_box = QListWidget()
        for item in self.curr_sources:
            if item != "":
                self.source_list_box.addItem(item)
        self.source_entry_box = QLineEdit()
        self.source_entry_box.setPlaceholderText('Enter New Data Source...')
        self.add_button = QPushButton(QIcon(':/qt-project.org/assistant/images/win/plus.png'), '')
        self.remove_button = QPushButton(QIcon(':/qt-project.org/assistant/images/win/minus.png'), '')
        self.button_layout = QVBoxLayout()
        self.button_layout.addWidget(self.add_button)
        self.button_layout.addWidget(self.remove_button)
        self.source_layout = QHBoxLayout()
        self.source_layout.addWidget(self.source_entry_box)
        self.source_layout.addLayout(self.button_layout)
        self.layout.addWidget(self.source_list_box)
        self.layout.addLayout(self.source_layout)
        self.add_button.clicked.connect(self.add_source)
        self.remove_button.clicked.connect(self.remove_source)

        # Ok/Cancel UI elements
        self.submit_layout = QHBoxLayout()
        self.submit_button = QPushButton('Ok')
        self.submit_button.clicked.connect(self.submit_values)
        self.submit_layout.addWidget(self.submit_button)
        self.cancel_button = QPushButton('Cancel')
        self.cancel_button.clicked.connect(self.close)
        self.submit_layout.addWidget(self.cancel_button)
        self.layout.addLayout(self.submit_layout)

        # list of elements to hide in the SourceDialog subclass - easier to keep here where I'm actually creating the elements
        self.HIDE_SOURCE_WIDGETS = [
                            self.proj_file_loc_label,
                            self.file_box,
                            self.file_button,
                            self.gpkg_template_checkbox,
                            self.gpkg_template_label,
                            self.gpkg_template_location_box,
                            self.gpkg_template_button,
                            self.gpkg_location_label,
                            self.gpkg_location_box,
                            self.gpkg_location_button,
                            self.proj_num_label,
                            self.proj_num_box,
                            self.proj_name_label,
                            self.proj_name_box,
                            self.loc_label,
                            self.loc_box,
                            self.client_label,
                            self.client_box,
                            ]

    # get save location for overall save file
    def getSaveFile(self):
        self.filename_dialog = QFileDialog()
        self.filename = self.filename_dialog.getSaveFileName(self, 'Specify Save Location:', self.home_path, 'QGIS Project File (*.qgz)')[0]
        self.file_box.setText(self.filename)

    # get gpkg templates if applicable
    def getGpkgTemplates(self):
        self.template_dialog = QFileDialog()
        self.gpkg_templates = self.template_dialog.getOpenFileNames(self, 'Select GeoPackage Template(s):', self.gpkg_path, 'GeoPackages (*.gpkg)')[0]
        self.gpkg_template_location_box.setText(str(self.gpkg_templates))

    # slot to control the visibility of gpkg UI elements
    def setGpkgVisibility(self, state):
        enabled = state == 2
        self.gpkg_template_location_box.setEnabled(enabled)
        self.gpkg_template_button.setEnabled(enabled)
        self.gpkg_location_box.setEnabled(enabled)
        self.gpkg_location_button.setEnabled(enabled)

    # determine where to save gpkgs from templates if applicable
    def getGpkgLocation(self):
        self.gpkg_location_dialog = QFileDialog()
        self.gpkg_location = self.gpkg_location_dialog.getExistingDirectory(self, 'Specify GeoPackage Save Location:', self.home_path)
        self.gpkg_location_box.setText(self.gpkg_location)
        
    def add_source(self):
        text = self.source_entry_box.text()
        if text:
            self.source_list_box.addItem(text)
            self.source_entry_box.clear()
        else:
            self.iface.messageBar().pushMessage('Source entry cannot be blank')

    def remove_source(self):
        selection = self.source_list_box.currentItem()
        if selection:
            self.source_list_box.takeItem(self.source_list_box.row(selection))
        else:
            self.iface.messageBar().pushMessage('No item selected')

    # gets the values from the various text boxes
    def submit_values(self):
        self.proj_num = self.proj_num_box.text()
        self.proj_name = self.proj_name_box.text()
        self.loc = self.loc_box.text()
        self.client = self.client_box.text()
        self.sources = ""
        for i in range(self.source_list_box.count()):
            if self.source_list_box.item(i).text() != "":
                self.sources = self.sources + self.source_list_box.item(i).text() + ";"
        self.success = True
        self.close()
        
    # this function is inherited by the subclass to hide UI elements not used when only adding data sources
    def hide_source_widgets(self):
        for item in self.HIDE_SOURCE_WIDGETS:
            item.hide()
