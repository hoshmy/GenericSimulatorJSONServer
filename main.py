import sys
from enum import Enum

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication

from main_widget import MainWidget


class _GeneralParameters(Enum):
    MAIN_WINDOW_HEIGHT = 300
    MAIN_WINDOW_WIDTH = 300
    MAIN_WINDOW_TITLE = 'Drone Simulator'


class HelloWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        main_window_size = QSize(_GeneralParameters.MAIN_WINDOW_WIDTH.value, _GeneralParameters.MAIN_WINDOW_HEIGHT.value)
        self.setMinimumSize(main_window_size)
        self.setWindowTitle(_GeneralParameters.MAIN_WINDOW_TITLE.value)

        self._init_ui()

    def _init_ui(self):
        central_widget = MainWidget(parent=self)
        self.setCentralWidget(central_widget)

        #
        # def _init_ui(self):
        #     central_widget = QWidget(self)
        #     self.setCentralWidget(central_widget)
        #     grid_layout = QGridLayout(self)
        #     central_widget.setLayout(grid_layout)
        #
        #     label2 = QtWidgets.QLabel('Hello World!')
        #     label2.setAlignment(QtCore.Qt.AlignCenter)
        #     self._text_edit = QtWidgets.QTextEdit()
        #     self._text_edit.setMaximumHeight(100)
        #     self._text_edit.setMaximumWidth(200)
        #     grid_layout.addWidget(label2, 0, 0)
        #     grid_layout.addWidget(self._text_edit, 1, 0)
        #     button = QPushButton('button')
        #     button.setText('send')
        #     grid_layout.addWidget(button, 2, 0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = HelloWindow()
    mainWin.show()
    sys.exit(app.exec_())







