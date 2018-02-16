import sys
from enum import Enum

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication

from main_widget import MainWidget


class _GeneralParameters(Enum):
    MAIN_WINDOW_HEIGHT = 500
    MAIN_WINDOW_WIDTH = 250
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = HelloWindow()
    mainWin.show()
    sys.exit(app.exec_())







