from PyQt5.QtGui import QIcon, QPixmap, QCursor
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
import threading
import time
import json
from socket import *
import socket
import sys

from secondWindow import SecondWindow


def styleButton(button):
    button.setCursor(Qt.PointingHandCursor)
    button.setStyleSheet(
        """QPushButton{background-color: rgb(249, 228, 183);
                    color: black;
                    border-radius: 15px;
                    font-family: 'Georgia';
                    font-size: 25px;
                    padding: 5px 0;}"""
        """QPushButton::hover
        {
        background-color : white;
        }
        """
    )

class FirstWindow(QWidget):
    switch_window = QtCore.pyqtSignal()
    def __init__(self, client_socket):
        super().__init__()
        self.client_socket = client_socket
        self.setWindowTitle("Halligalli Game")
        self.setGeometry(0, 0, 900, 600)

        self.image = QPixmap("images/title.png")
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setPixmap(self.image)

        self.start_button = QPushButton("게임시작")

        self.start_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.start_button.setStyleSheet(
            """QPushButton{background-color: rgb(249, 228, 183);
            color: black;
            border-radius: 25px;
            font-family: 'Georgia';
            font-size: 40px;
            margin-bottom: 5px;
            padding: 8px 0;}"""
            """QPushButton::hover
            {
            background-color : white;
            }
            """
        )
        self.start_button.clicked.connect(self.secondWindowEmit)


        self.grid = QGridLayout()
        self.grid.addWidget(self.label, 1, 1)
        self.grid.addWidget(self.start_button, 2, 1)
        self.setLayout(self.grid)
        self.show()


    def secondWindowEmit(self):
        self.client_socket.connect(('220.149.128.100', 4061))
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()
        self.switch_window.emit()

    def run(self): # 플레이어 데이터 받아옴
        while True:
            self.recv_data = self.client_socket.recv(1024)
            self.recv_data = json.loads(self.recv_data.decode())
            time.sleep(0.1)
            if(self.recv_data.get('id') != None):
                player_id = self.recv_data.get('id')
                player_card = self.recv_data.get('card')
                print(player_id, player_card)
