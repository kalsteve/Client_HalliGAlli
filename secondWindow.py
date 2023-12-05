from PyQt5.QtGui import QIcon, QPixmap, QCursor
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import json
import threading
import time
from socket import *
import socket
import sys


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
class SecondWindow(QWidget):
    def __init__(self, client_socket):
        super().__init__()
        self.client_socket = client_socket




        self.player_cards = ['banana1', 'orange1', 'strawberry1', 'abocado1'] #예시임. 서버에서 값 받아와야함
        self.current_index = 0

        self.setWindowTitle("Halligalli Game")
        self.setGeometry(0, 0, 1000, 800)

        self.player()
        self.show()

    def player(self):
        imageLayout = QGridLayout()

        self.bell_img = QLabel(self)
        self.bell_img.setPixmap(QPixmap('images/bell.png'))
        imageLayout.addWidget(self.bell_img, 1, 1)

        self.my_backcard = QLabel(self)
        self.my_backcard.setPixmap(QPixmap('images/back.png'))
        imageLayout.addWidget(self.my_backcard, 3, 1)

        self.player2_backcard = QLabel(self)
        self.player2_backcard.setPixmap(QPixmap('images/back.png'))
        imageLayout.addWidget(self.player2_backcard, 1, 0)

        self.player3_backcard = QLabel(self)
        self.player3_backcard.setPixmap(QPixmap('images/back.png'))
        imageLayout.addWidget(self.player3_backcard, 0, 1)

        self.player4_backcard = QLabel(self)
        self.player4_backcard.setPixmap(QPixmap('images/back.png'))
        imageLayout.addWidget(self.player4_backcard, 1, 2)

        self.my_openedcard = QLabel()
        self.pixmap = QPixmap(self.player_cards[self.current_index] + '.jpg')
        self.my_openedcard.setPixmap(self.pixmap)
        imageLayout.addWidget(self.my_openedcard, 2, 1)

        self.open_button = QPushButton('카드 넘기기')
        self.open_button.clicked.connect(self.open_card)
        styleButton(self.open_button)
        imageLayout.addWidget(self.open_button, 4, 1)

        self.bell_button = QPushButton('종 울리기')
        self.bell_button.clicked.connect(self.bell)
        styleButton(self.bell_button)
        imageLayout.addWidget(self.bell_button, 4, 2)

        self.setLayout(imageLayout)

    def bell(self,client_socket): # 종 울리기 함수
        data = json.dumps({'Action': 'Bell'})
        self.client_socket.sendall(data.encode())
        print('bell')


    def open_card(self,client_socket): #카드 넘기는 함수
        self.current_index = (self.current_index + 1) % len(self.player_cards)
        self.pixmap = QPixmap('images/' + self.player_cards[self.current_index] + '.jpg')
        self.my_openedcard.setPixmap(self.pixmap)
        data = json.dumps({'Action': 'Draw'})
        self.client_socket.sendall(data.encode())

    def closeEvent(self, event): #창 종료시 소켓 종료
        self.client_socket.close()
        event.accept()
