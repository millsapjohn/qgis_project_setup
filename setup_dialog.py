from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel
from qgis.utils import iface

class SetupDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.iface = iface
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

        self.submit_button = QPushButton('Ok')
        self.submit_button.clicked.connect(self.submit_values)
        self.layout.addWidget(self.submit_button)

        self.cancel_button = QPushButton('Cancel')
        self.cancel_button.clicked.connect(self.close)
        self.layout.addWidget(self.cancel_button)

    def submit_values(self):
        proj_num = self.proj_num_box.text()
        self.iface.messageBar().pushMessage(proj_num)
        self.close()
