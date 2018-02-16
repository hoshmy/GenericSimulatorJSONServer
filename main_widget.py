import os
from enum import Enum

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot

from udp_server import UDPServer


class _Parameter(Enum):
    MESSAGES_FOLDER = 'messages'
    REGULAR_LABEL_MAX_WIDTH = 200
    REGULAR_LABEL_MAX_HEIGHT = 20
    GRID_LAYOUT_VERTICAL_SPACING = 1


class WidgetId(Enum):
    HEADER = 0
    MESSAGES_SELECT_COMBO_BOX = 1
    CURRENT_MESSAGE_TEXT_EDIT = 2
    SEND_BUTTON = 3
    RECEIVED_MESSAGE_HEADER = 4
    RECEIVED_MESSAGE_BODY = 5
    NUMBER_OF_WIDGETS = 6


class MainWidget(QWidget):

    _signal_send_via_communication = pyqtSignal('QString')

    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)

        self._udp_server = UDPServer()
        self._messages = []
        self._encoded_messages = []
        self._messages_names = []
        self._widgets = [None] * WidgetId.NUMBER_OF_WIDGETS.value

        self._parse_messages()
        self._init_ui()
        self._init_connections()

        # reset state
        self._slot_on_message_list_index_changed(0)

    def _init_connections(self):
        self._signal_send_via_communication.connect(self._udp_server.slot_send)
        self._widgets[WidgetId.SEND_BUTTON.value].clicked.connect(self._slot_on_click)
        self._widgets[WidgetId.MESSAGES_SELECT_COMBO_BOX.value].currentIndexChanged.connect(
                self._slot_on_message_list_index_changed
        )
        self._udp_server.signal_message_received.connect(self._slot_on_message_received)

    def _init_ui(self):
        grid_layout = QGridLayout(self)
        grid_layout.setVerticalSpacing(_Parameter.GRID_LAYOUT_VERTICAL_SPACING.value)
        self.setLayout(grid_layout)

        self._widgets[WidgetId.HEADER.value] = QLabel('Chose a message from list:')
        self._widgets[WidgetId.HEADER.value].setAlignment(QtCore.Qt.AlignLeft)
        self._widgets[WidgetId.HEADER.value].setMaximumSize(
                _Parameter.REGULAR_LABEL_MAX_WIDTH.value,
                _Parameter.REGULAR_LABEL_MAX_HEIGHT.value
        )

        self._widgets[WidgetId.MESSAGES_SELECT_COMBO_BOX.value] = QComboBox()
        self._widgets[WidgetId.MESSAGES_SELECT_COMBO_BOX.value].addItems(self._messages_names)

        self._widgets[WidgetId.CURRENT_MESSAGE_TEXT_EDIT.value] = QTextEdit()
        self._widgets[WidgetId.CURRENT_MESSAGE_TEXT_EDIT.value].setMaximumHeight(100)
        self._widgets[WidgetId.CURRENT_MESSAGE_TEXT_EDIT.value].setMaximumWidth(200)

        self._widgets[WidgetId.SEND_BUTTON.value] = QPushButton('button')
        self._widgets[WidgetId.SEND_BUTTON.value].setText('send')

        self._widgets[WidgetId.RECEIVED_MESSAGE_HEADER.value] = QLabel('Last received message:')
        self._widgets[WidgetId.RECEIVED_MESSAGE_HEADER.value].setAlignment(QtCore.Qt.AlignLeft)
        self._widgets[WidgetId.RECEIVED_MESSAGE_HEADER.value].setMaximumSize(
                _Parameter.REGULAR_LABEL_MAX_WIDTH.value,
                _Parameter.REGULAR_LABEL_MAX_HEIGHT.value
        )

        self._widgets[WidgetId.RECEIVED_MESSAGE_BODY.value] = QLabel('None')
        self._widgets[WidgetId.RECEIVED_MESSAGE_BODY.value].setMaximumHeight(100)
        self._widgets[WidgetId.RECEIVED_MESSAGE_BODY.value].setMaximumWidth(200)
        self._set_data_label_style(self._widgets[WidgetId.RECEIVED_MESSAGE_BODY.value])

        for i, widget in enumerate(self._widgets):
            grid_layout.addWidget(widget, i, 0)

    def _parse_messages(self):
        if os.path.exists(_Parameter.MESSAGES_FOLDER.value):
            for root, dirs, files in os.walk(_Parameter.MESSAGES_FOLDER.value):
                for file in files:
                    path_to_file = os.path.join(_Parameter.MESSAGES_FOLDER.value, file)
                    with open(path_to_file, 'r') as current_message_file:
                        current_message = current_message_file.read()
                        current_message_striped = current_message.strip()
                        current_message_encoded = current_message_striped.encode()

                        self._messages.append(current_message)
                        self._encoded_messages.append(current_message_encoded)
                        file_name_without_extention = file.split('.')[0]
                        self._messages_names.append(file_name_without_extention)

    def _set_data_label_style(self, label):
        # label.setAlignment(Qt.AlignLeft | Qt.AlignVTop)
        label.setAlignment(Qt.AlignLeft)
        label.setFrameShape(QFrame.Panel)
        label.setLineWidth(1)

    @pyqtSlot(int)
    def _slot_on_message_list_index_changed(self, message_index):
        current_selected_message = self._messages[message_index]
        self._widgets[WidgetId.CURRENT_MESSAGE_TEXT_EDIT.value].setText(current_selected_message)


    @pyqtSlot()
    def _slot_on_click(self):
        current_text = self._widgets[WidgetId.CURRENT_MESSAGE_TEXT_EDIT.value].toPlainText()
        current_text_striped = current_text.strip()
        self._signal_send_via_communication.emit(current_text_striped)

    @pyqtSlot('QString')
    def _slot_on_message_received(self, message):
        self._widgets[WidgetId.RECEIVED_MESSAGE_BODY.value].setText(message)