# client.py
import socket
import json
import threading

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QMessageBox, QGridLayout, QFrame, QDialog, QDialogButtonBox
from PyQt5.QtCore import Qt, QTimer

from DataConverter import DataConverter

''' 1. ready 버튼을 누르면 서버에서 시작할건지 말건지 알려주면 창이 띄어져야 함.
        만약 혼자인 상태에서 ready를 누르면 아무것도 안뜨고 ready만 박히게 
    2. 서버에서 보내는 데이터를 받을 때 코드 수정해야함. -> receive_data 함수
    3. 서버에 데이터 보낼때 보내는 형식 아마 수정해야할거임 -> send 함수 찾아서.
    4. '''

class HarigariClient(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initMainMenu()

        # 통신 설정
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect(('kiwiwip.duckdns.org', 4848))
        self.thread_locker = threading.Lock()
        self.thread_locker.locked()
        self.data = self.first_receive(self.clientSocket)

        # 카드 라벨 설정
        self.card_labels = [QLabel(self) for _ in range(4)]

        # 사용하는 버튼
        self.draw_card_button: QPushButton = None
        self.bell_button: QPushButton = None

        # 턴 라벨
        self.turn_label = QLabel(self)
        self.turn_label.setAlignment(Qt.AlignCenter)
        self.turn_label.setStyleSheet("color: white; font-size: 18px;")

        """self.timer = QTimer(self)
        self.timer.timeout.connect(self.sendSignalToServer)
        self.timer.start(10)  # Set the timeout interval to 5000 milliseconds (5 seconds)
"""

    def initMainMenu(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        image_label = QLabel(self)
        image_label.setPixmap(QPixmap('images/title.png'))  # Replace with the actual path to your image
        image_label.setAlignment(Qt.AlignCenter)  # Center the image
        image_label.setScaledContents(True)

        # 게임 시작 버튼
        self.game_start_button = QPushButton('Game Start', self)
        self.game_start_button.clicked.connect(self.showGameScreen)
        self.game_start_button.setEnabled(False)

        # 레디 버튼
        self.ready_button = QPushButton('Ready', self)
        self.ready_button.clicked.connect(self.showReadyScreen)

        # 레이아웃 설정
        layout = QVBoxLayout(self.central_widget)
        layout.addWidget(image_label)
        layout.addWidget(self.game_start_button)
        layout.addWidget(self.ready_button)

        # 제목과 크기
        self.setWindowTitle('Halli Galli')
        self.setFixedSize(600, 800)

    def initGameScreen(self):
        thread = threading.Thread(target=self.in_game_receive_data, args=(self.data,))
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Set background color to green
        self.central_widget.setStyleSheet("background-color: green;")

        # Create labels for images
        bell_image_label = QLabel(self)
        bell_image_label.setPixmap(QPixmap('images/bell.png'))
        bell_image_label.setAlignment(Qt.AlignCenter)  # Center the bell image

        # Create separator lines with red color and thicker lines
        separator_lines = [
            QFrame(self, frameShape=QFrame.HLine, frameShadow=QFrame.Sunken, lineWidth=5),
            QFrame(self, frameShape=QFrame.VLine, frameShadow=QFrame.Sunken, lineWidth=5),
            QFrame(self, frameShape=QFrame.VLine, frameShadow=QFrame.Sunken, lineWidth=5),
            QFrame(self, frameShape=QFrame.VLine, frameShadow=QFrame.Sunken, lineWidth=5)
        ]

        for line in separator_lines:
            line.setStyleSheet("background-color: red;")

        # Create back_image labels for each player with some spacing
        back_image_labels = [QLabel(self) for _ in range(4)]
        for label in back_image_labels:
            label.setPixmap(QPixmap('images/back.png'))

        # Create bell button
        self.bell_button = QPushButton('Ring Bell', self)
        self.bell_button.clicked.connect(self.sendBellAction)
        self.bell_button.setStyleSheet("background-color: white;")
        self.bell_button.setEnabled(False)

        # Create draw card button
        self.draw_card_button = QPushButton('Draw Card', self)
        self.draw_card_button.clicked.connect(self.drawCardAction)
        self.draw_card_button.setStyleSheet("background-color: white;")
        self.draw_card_button.setEnabled(False)

        # Create label for current player's turn
        self.turn_label = QLabel(self)
        self.turn_label.setAlignment(Qt.AlignCenter)
        self.turn_label.setStyleSheet("color: white; font-size: 18px;")

        # Create layout
        layout = QGridLayout(self.central_widget)
        layout.addWidget(self.turn_label, 0, 0, 1, 4)  # Row 0, Column 0, Span 1 row, 4 columns
        layout.addWidget(bell_image_label, 1, 0, 1, 4)  # Row 1, Column 0, Span 1 row, 4 columns
        layout.addWidget(separator_lines[0], 2, 0, 1, 4)  # Row 2, Column 0, Span 1 row, 4 columns

        # Add labels for each player with some spacing
        player_labels = [QLabel(f'   Player {i+1}') for i in range(4)]
        for i, label in enumerate(player_labels):
            layout.addWidget(label, 3, i)  # Row 3, Column i

        # Add vertical separator lines between players
        for i, line in enumerate(separator_lines[1:], start=1):
            layout.addWidget(line, 2, i, 5, 1)  # Row 2, Column i, Span 5 rows, 1 column

        # Add back_image labels for each player in the same row as my_back_image
        for i, label in enumerate(back_image_labels):
            layout.addWidget(label, 4, i, 1, 1)  # Row 4, Column i, Span 1 row, 1 column

        # Add bell button
        layout.addWidget(self.bell_button, 6, 0, 1, 2)  # Row 6, Column 0, Span 1 row, 2 columns

        # Add draw card button
        layout.addWidget(self.bell_button, 6, 2, 1, 2)  # Row 6, Column 2, Span 1 row, 2 columns

        self.setWindowTitle('Halli Galli')
        self.setFixedSize(600, 800)  # Set fixed size for the window
        self.show()

    # 서버에 신호를 보냄
    def first_receive(self, client_socket: socket.socket):
        print("Signal sent to server")
        return DataConverter(self.clientSocket.recv(1024, socket.MSG_WAITALL))

    def receive_action(self, data: DataConverter):
        data.recv(self.clientSocket.recv(1024, socket.MSG_WAITALL))
        print(f"Received action from server: {data: str}")

    def receive_data(self, data: DataConverter):
        if data is None:
            print("No data received")
            return None

        data.recv(self.clientSocket.recv(1024, socket.MSG_WAITALL))
        print(f"Received data from server: {data: str}")

        player_list = data.get_player_list()

        current_player = data.player_turn()
        player_list = data.get_player_list()

        # 카드 정보가 있으면
        for player, card_label in player_list, self.card_labels:
            path = f'images/{player["card"]["type"].lower()}{player_list["card"]["volume"]}.jpg'
            card_image_path = f'images/{path}'
            card_label.setPixmap(QPixmap(card_image_path))

            # 화면 상단에 현재 플레이어 누군지 표시
            self.turn_label.setText(f"Current Turn: {current_player}")

    def in_game_communicate(self, data: DataConverter):
        self.bell_button.setEnabled(True)
        while True:
            data.recv(self.clientSocket.recv(1024, socket.MSG_WAITALL))
            # 플레이어의 턴인 상태면
            if data.get_action() == data.player_action["PLAYER_TURN"]:
                print(f"Received data from server: {data: str}")
                self.draw_card_button.setEnabled(True)
                continue

            # 플레이어가 인게임 상태면
            if data.my_action == data.player_action["PLAYER_GAMING"]:
                print(f"Received data from server: {data: str}")
                player_list = data.get_player_list()
                current_player_turn = data.player_turn()

                # 카드 정보가 있으면
                for player, card_label in player_list, self.card_labels:
                    path = f'images/{player["card"]["type"].lower()}{player_list["card"]["volume"]}.jpg'
                    card_image_path = f'images/{path}'
                    card_label.setPixmap(QPixmap(card_image_path))

                    # 화면 상단에 현재 플레이어 누군지 표시
                    self.turn_label.setText(f"Current Turn: {current_player_turn}")


    # 카드를 뽑는 액션, 객체를 받아서 서버에 전송
    def drawCardAction(self, data: DataConverter):
        self.thread_locker.acquire()
        self.clientSocket.sendall(bytes(data.send("PLAYER_DRAW")), socket.MSG_WAITALL)
        self.thread_locker.release()
        print(f"Draw Card pressed! \n send = {data: str}", end="\n")

    def sendBellAction(self, data: DataConverter):
        self.thread_locker.acquire()
        self.clientSocket.sendall(bytes(data.send("PLAYER_BELL")), socket.MSG_WAITALL)
        self.thread_locker.release()
        print(f"Bell pressed! \n send = {data: str}", end="\n")

    # 밸 눌렀을때 확인용? - 확인 부탁
    def handleBellPress(self):
        print("Bell pressed!")

    # 카드를 뽑았을때 확인용? - 확인 부탁
    def handleCardTransfer(self):
        print("Card transfer initiated!")

    # 게임 화면을 보여줌
    def showGameScreen(self):
        self.initGameScreen()
        self.show()

    # 준비 버튼을 누르면 게임 시작 버튼이 활성화됨
    def showReadyScreen(self):
        self.ready_button.setStyleSheet("color: red;")
        # Create a confirmation dialog
        dialog = ReadyConfirmationDialog(self, self.clientSocket, self.data)
        result = dialog.exec_()

        self.clientSocket.sendall(bytes(self.data.send("PLAYER_READY")), socket.MSG_WAITALL)
        self.data.recv(self.clientSocket.recv(1024, socket.MSG_WAITALL))
        self.receive_action(self.data)

        if result == QDialog.Accepted:
            # 게임 시작 버튼 활성화
            self.game_start_button.setEnabled(True)
        else:
            # 레디 버튼 색상 원래대로
            self.ready_button.setStyleSheet("color: original;")

    # 게임 화면을 닫으면 소켓도 닫힘
    def closeEvent(self, event):
        self.clientSocket.close()
        event.accept()
        socket.close()

# 레디 버튼을 누르면 뜨는 창
class ReadyConfirmationDialog(QDialog):
    def __init__(self, thread_lock: threading.Lock, sock: socket.socket, data: DataConverter , parent=None):
        super(ReadyConfirmationDialog, self).__init__(parent)
        self.sock: socket.socket = sock
        self.data: DataConverter = data
        self.thread_lock: threading.Lock = thread_lock

        self.setWindowTitle('Ready Confirmation')
        self.setMinimumWidth(300)

        # 버튼을
        button_box = QDialogButtonBox(QDialogButtonBox.Yes | QDialogButtonBox.No)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel('다른 플레이어를 기다릴까요?'))
        layout.addWidget(button_box)

    # 게임 다른 플레이어를 기다림
    def accept(self):
        self.sock.sendall(bytes(self.data.send("PLAYER_READY")), socket.MSG_WAITALL)
        self.data.recv(self.sock.recv(1024, socket.MSG_WAITALL))
        if self.data.get_action() != self.data.player_action["PLAYER_GAMING"]:

        super(ReadyConfirmationDialog, self).accept()

    # 다른 플레이어를 기다리지 않음
    def reject(self):
        self.sock.sendall(bytes(self.data.send("PLAYER_NOT_WANT")), socket.MSG_WAITALL)
        self.data.recv(self.sock.recv(1024, socket.MSG_WAITALL))

        while True:
            if(self.data.get_action() == self.data.player_action["PLAYER_GAMING"]):
                break
            elif(self.data.get_action() == self.data.player_action["PLAYER_TURN"]):
                break

        self.thread_lock.release()

        super(ReadyConfirmationDialog, self).reject()



if __name__ == '__main__':
    app = QApplication([])
    client = HarigariClient()
    client.show()
    app.exec_()
