from qgis.utils import iface
from PyQt5.QtWidgets import QDialog, QListWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QIcon

class ConnectionDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.iface = iface
        self.initUI()
        self.success = False

    def initUI(self):
        self.setWindowTitle('Add/Remove Persistent GeoPackage Connections:')
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.connections_layout = QHBoxLayout()
        self.current_layout = QVBoxLayout()
        self.persistent_layout = QVBoxLayout()
        self.connections_buttons_layout = QVBoxLayout()
        self.finished_buttons_layout = QHBoxLayout()

        self.current_label = QLabel('Current GeoPackage Connections')
        self.persistent_label = QLabel('Persistent Project GeoPackage Connections')
        self.current_connections_box = QListWidget()
        self.persistent_connections_box = QListWidget()

        self.current_layout.addWidget(self.current_label)
        self.current_layout.addWidget(self.current_connections_box)

        self.persistent_layout.addWidget(self.persistent_label)
        self.persistent_layout.addWidget(self.persistent_connections_box)

        self.add_button = QPushButton(QIcon(':/images/themes/default/mActionArrowRight.svg'), '')
        self.remove_button = QPushButton(QIcon(':/images/themes/default/mActionArrowLeft.svg'), '')
        self.connections_buttons_layout.addWidget(self.add_button)
        self.connections_buttons_layout.addWidget(self.remove_button)

        self.connections_layout.addLayout(self.current_layout)
        self.connections_layout.addLayout(self.connections_buttons_layout)
        self.connections_layout.addLayout(self.persistent_layout)

        self.layout.addLayout(self.connections_layout)

        self.ok_button = QPushButton(text='Ok')
        self.ok_button.clicked.connect(self.submit_values)
        self.cancel_button = QPushButton(text='Cancel')
        self.cancel_button.clicked.connect(self.close)
        self.finished_buttons_layout.addWidget(self.ok_button)
        self.finished_buttons_layout.addWidget(self.cancel_button)

        self.layout.addLayout(self.finished_buttons_layout)

    def submit_values(self):
        pass
