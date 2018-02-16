from threading import Thread
import socket
import time
import select
from enum import Enum

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QThread


class _Parameters(Enum):
    PORT = 5005
    UDP_IP = '127.0.0.1'
    CONNECTION_MESSAGE_REQUEST = 'connect'
    CONNECTION_MESSAGE_RESPONSE = 'connect'


class UDPServer(QThread):

    signal_message_received = pyqtSignal('QString')

    def __init__(self, parent=None):
        QThread.__init__(self, parent)

        self._exiting = False

        self._sock = None
        self._sleep_time = 0.001
        self._client_address = None
        self._message_id = 1
        self._communication_thread_keep_running = True
        self._is_connected = False

        self._init_communication()
        self.start()

    def __del__(self):
        self.exiting = True
        self.wait()

        if self._sock:
            self._sock.close()

    def _init_communication(self):
        print('init communication')

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.bind((_Parameters.UDP_IP.value, _Parameters.PORT.value))

    def run(self):
        self._log('start communication thread')
        self._initial_connection_loop()
        self._do_communication()

    def _do_communication(self):
        while self._communication_thread_keep_running:
            readable, writable, exceptional = select.select([self._sock], [], [])
            if readable:
                data, self._client_address = self._sock.recvfrom(1024)
                decoded_data = data.decode()
                self._log(decoded_data)
                if decoded_data == _Parameters.CONNECTION_MESSAGE_REQUEST.value:
                    self._log('Reconnect from {}'.format(self._client_address))
                    self._sock.sendto(_Parameters.CONNECTION_MESSAGE_RESPONSE.value.encode(), self._client_address)
                else:
                    self.signal_message_received.emit(decoded_data)

            time.sleep(self._sleep_time)

    def _initial_connection_loop(self):
        print('waiting for first connection')
        while not self._is_connected:
            data, self._client_address = self._sock.recvfrom(1024)

            data = data.decode()
            self._log("received message: {}".format(data))
            if data == _Parameters.CONNECTION_MESSAGE_REQUEST.value:
                print('Established communication from {}'.format(self._client_address))
                number_of_bytes_sent = self._sock.sendto(_Parameters.CONNECTION_MESSAGE_RESPONSE.value.encode(), self._client_address)

                self._log('number_of_bytes_sent: {}'.format(number_of_bytes_sent))

                self._is_connected = True
            else:
                print('during initial communication received a non connect message')

    @pyqtSlot('QString')
    def slot_send(self, message):
        if self._is_connected:
            self._log('sending {}'.format(message))
            self._sock.sendto(message.encode(), self._client_address)
        else:
            self._log('Not connected yet, the message was {}'.format(message))

    def _log(self, message):
        print('UDPServer: {}'.format(message))






