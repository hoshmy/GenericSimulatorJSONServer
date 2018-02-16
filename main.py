import sys
from enum import Enum

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal

from udp_server import UDPServer


class GeneralParameters(Enum):
    MAIN_WINDOW_HEIGHT = 300
    MAIN_WINDOW_WIDTH = 300


class HelloWindow(QMainWindow):

    _signal_send_via_communication = pyqtSignal('QString')

    def __init__(self):
        QMainWindow.__init__(self)
        main_window_size = QSize(GeneralParameters.MAIN_WINDOW_WIDTH.value, GeneralParameters.MAIN_WINDOW_HEIGHT.value)
        self.setMinimumSize(main_window_size)
        self.setWindowTitle("Drone Simulator")

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        grid_layout = QGridLayout(self)
        central_widget.setLayout(grid_layout)

        label0 = QtWidgets.QLabel('Hello World!')
        label0.setAlignment(QtCore.Qt.AlignCenter)
        label1 = QtWidgets.QLabel('Hello World!')
        label1.setAlignment(QtCore.Qt.AlignCenter)

        grid_layout.addWidget(label0, 0, 0)
        grid_layout.addWidget(label1, 1, 0)
        label2 = QtWidgets.QLabel('Hello World!')
        label2.setAlignment(QtCore.Qt.AlignCenter)
        self._text_edit = QtWidgets.QTextEdit()
        self._text_edit.setMaximumHeight(100)
        self._text_edit.setMaximumWidth(200)
        grid_layout.addWidget(label2, 0, 1)
        grid_layout.addWidget(self._text_edit, 1, 1)
        button = QPushButton('button')
        button.setText('send')
        grid_layout.addWidget(button, 2, 1)

        button.clicked.connect(self.on_click)

        self._udp_server = UDPServer()
        self._signal_send_via_communication.connect(self._udp_server.slot_send)

    @pyqtSlot()
    def on_click(self):
        current_text = self._text_edit.toPlainText().strip()
        print('emitting {}'.format(current_text))
        self._signal_send_via_communication.emit(current_text)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = HelloWindow()
    mainWin.show()
    sys.exit(app.exec_())







