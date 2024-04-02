from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QListWidget, QHBoxLayout
from PyQt5.QtGui import QIcon
from qgis.utils import iface

class SetupDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.iface = iface
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Project Setup')
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.proj_num_label = QLabel('Project Number: ')
        self.layout.addWidget(self.proj_num_label)
        self.proj_num_box = QLineEdit()
        self.layout.addWidget(self.proj_num_box)

        self.proj_name_label = QLabel('Project Name: ')
        self.layout.addWidget(self.proj_name_label)
        self.proj_name_box = QLineEdit()
        self.layout.addWidget(self.proj_name_box)

        self.client_label = QLabel('Client: ')
        self.layout.addWidget(self.client_label)
        self.client_box = QLineEdit()
        self.layout.addWidget(self.client_box)

        self.loc_label = QLabel('Project Location: ')
        self.layout.addWidget(self.loc_label)
        self.loc_box = QLineEdit()
        self.layout.addWidget(self.loc_box)

        self.source_label = QLabel('Data Sources: ')
        self.layout.addWidget(self.source_label)
        self.source_list_box = QListWidget()
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

        self.submit_layout = QHBoxLayout()
        self.submit_button = QPushButton('Ok')
        self.submit_button.clicked.connect(self.submit_values)
        self.submit_layout.addWidget(self.submit_button)

        self.cancel_button = QPushButton('Cancel')
        self.cancel_button.clicked.connect(self.close)
        self.submit_layout.addWidget(self.cancel_button)
        self.layout.addLayout(self.submit_layout)

        self.HIDE_WIDGETS = [
                            self.proj_num_label, 
                            self.proj_num_box, 
                            self.proj_name_label, 
                            self.proj_name_box, 
                            self.loc_label, 
                            self.loc_box, 
                            self.client_label, 
                            self.client_box,
                            ]
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

    def submit_values(self):
        self.close()
        
    def hide_widgets(self):
        for item in self.HIDE_WIDGETS:
            item.hide()
