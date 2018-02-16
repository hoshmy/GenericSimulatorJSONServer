from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot

from udp_server import UDPServer


class MainWidget(QWidget):

    _signal_send_via_communication = pyqtSignal('QString')

    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self._udp_server = UDPServer()

        self._init_ui()
        self._init_connections()

    def _init_connections(self):
        self._signal_send_via_communication.connect(self._udp_server.slot_send)

    def _init_ui(self):
        grid_layout = QGridLayout(self)
        self.setLayout(grid_layout)

        label2 = QLabel('Hello World!')
        label2.setAlignment(QtCore.Qt.AlignCenter)
        self._text_edit = QTextEdit()
        self._text_edit.setMaximumHeight(100)
        self._text_edit.setMaximumWidth(200)
        grid_layout.addWidget(label2, 0, 0)
        grid_layout.addWidget(self._text_edit, 1, 0)
        button = QPushButton('button')
        button.setText('send')
        grid_layout.addWidget(button, 2, 0)

        button.clicked.connect(self.on_click)

    @pyqtSlot()
    def on_click(self):
        current_text = self._text_edit.toPlainText().strip()
        print('emitting {}'.format(current_text))
        self._signal_send_via_communication.emit(current_text)