# client.py
import socket
import json
import threading

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QMessageBox, \
    QGridLayout, QFrame, QDialog, QDialogButtonBox
from PyQt5.QtCore import Qt, QTimer, QThread, QObject, pyqtSlot, pyqtSignal, QSize

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

        self.data = self.first_receive(self.clientSocket)

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
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Set background color to green
        self.central_widget.setStyleSheet("background-color: green;")

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
        self.bell_button.clicked.connect(self.handleBellPress)
        # 벨의 이미지를 버튼으로 사용하고 크기는 이미지에 맞게 변경
        self.bell_button.setStyleSheet("border-image: url(images/bell.png); background-color: white;")
        self.bell_button.setEnabled(False)

        # Create draw card button
        bell_icon = QPixmap('images/bell.png')
        self.draw_card_button = QPushButton('Draw Card', self)
        self.draw_card_button.clicked.connect(self.handleDrawCard)
        self.draw_card_button.setStyleSheet("background-color: white;")
        self.draw_card_button.setEnabled(False)

        # Create label for current player's turn
        self.turn_label = QLabel(self)
        self.turn_label.setAlignment(Qt.AlignCenter)
        self.turn_label.setStyleSheet("color: white; font-size: 18px;")

        # Create layout
        layout = QGridLayout(self.central_widget)
        layout.addWidget(self.turn_label, 0, 0, 1, 4)  # Row 0, Column 0, Span 1 row, 4 columns
        # layout.addWidget(bell_image_label, 1, 0, 1, 4)  # Row 1, Column 0, Span 1 row, 4 columns
        layout.addWidget(separator_lines[0], 2, 0, 1, 4)  # Row 2, Column 0, Span 1 row, 4 columns
        layout.addWidget(self.draw_card_button, 3, 0, 1, 2)  # Row 3, Column 0, Span 1 row, 2 columns
        layout.addWidget(self.bell_button, 1, 0, 1, 4)  # Row 3, Column 2, Span 1 row, 2 columns

        # Add labels for each player with some spacing
        player_labels = [QLabel(f'   Player {i + 1}') for i in range(4)]
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

        self.bell_button.setEnabled(True)

        self.setWindowTitle('Halli Galli')
        self.setFixedSize(600, 800)  # Set fixed size for the window
        self.show()

    # 서버에 신호를 보냄
    def first_receive(self, client_socket: socket.socket):
        print("Signal sent to server")
        data = DataConverter(self.clientSocket.recv(1024, socket.MSG_WAITALL))
        print("Received data from server: ", data)
        return data

    def receive_action(self, data: DataConverter):
        data.recv(self.clientSocket.recv(1024, socket.MSG_WAITALL))
        print("Received action from server:", data)



        # 카드를 뽑는 액션, 객체를 받아서 서버에 전송

    # 카드를 뽑았을때
    def handleDrawCard(self):
        self.game_thread.update_event(clicked_draw_button=True)
        print("Draw card pressed!")

    # 밸 눌렀을때
    def handleBellPress(self):
        self.game_thread.update_event(clicked_bell_button=True)
        print("Bell pressed!")

    def handleCardTransfer(self):
        print("Card transfer initiated!")

    def handleMyTurn(self):
        self.draw_card_button.setEnabled(True)
        print("My turn!")

    def handleNotMyTurn(self):
        self.draw_card_button.setEnabled(False)
        print("Not my turn!")

    def handlePlayerReady(self, action):
        # 'PLAYER_NOT_WANT' 액션 처리
        self.data.set_action(action)
        self.clientSocket.sendall(bytes(self.data))
        print("set action: ", self.data.get_action())
        self.data.recv(self.clientSocket.recv(1024, socket.MSG_WAITALL))
        print("Received action from server:", self.data)

    # 게임 화면을 보여줌
    def showGameScreen(self):
        self.game_thread = InGameThread(parent=self, client_socket=self.clientSocket, data=self.data)
        self.game_thread.cardUpdateSignal.connect(self.receive_data)
        self.game_thread.myTurnSignal.connect(self.handleMyTurn)
        self.game_thread.notMyTurnSignal.connect(self.handleNotMyTurn)
        self.game_thread.start()


        self.initGameScreen()
        self.show()

    # 준비 버튼을 누르면 게임 시작 버튼이 활성화됨
    def showReadyScreen(self):
        self.ready_button.setStyleSheet("color: red;")

        # Create a confirmation dialog
        dialog = ReadyConfirmationDialog(self)
        dialog.playerReadySignal.connect(self.handlePlayerReady)
        result = dialog.exec_()

        if result == QDialog.Rejected:
            # 레디버튼 비활성화, 게임시작버튼 활성화
            self.ready_button.setEnabled(False)
            self.game_start_button.setEnabled(True)

        elif result == QDialog.Accepted:
            # 레디버튼 비활성화
            self.ready_button.setEnabled(False)

            wait_dialog = WaitingDialog(self)
            waitThread = QThread()
            waitThread.run = self.handlePlayerWaiting
            waitThread.start()
            wait_dialog.exec_()

            # 게임시작버튼 활성화
            self.game_start_button.setEnabled(True)

    def receive_data(self, data: DataConverter):
        current_player = data.get_turn()
        player_list = data.get_player_list()

        # 카드 정보가 있으면
        for player, card_label in player_list, self.card_labels:
            path = f'images/{player["card"]["type"].lower()}{player_list["card"]["volume"]}.jpg'
            print(path)
            card_image_path = f'images/{path}'
            card_label.setPixmap(QPixmap(card_image_path))

            # 화면 상단에 현재 플레이어 누군지 표시
            self.turn_label.setText(f"Current Turn: {current_player}")

        self.data = data

    def handlePlayerWaiting(self):
        wait_qthread = QThread()
        wait_qthread.run = lambda: self.data.recv(self.clientSocket.recv(1024, socket.MSG_WAITALL))
        wait_qthread.start()

        while True:
            if wait_qthread.isFinished():
                if self.data.get_action() == self.data.player_action["PLAYER_GAMING"]:
                    print("Received action from server:", self.data)
                    print("게임이 시작됨")
                    break
            QApplication.processEvents()  # 이벤트 루프 강제 처리

    # 게임 화면을 닫으면 소켓도 닫힘
    def closeEvent(self, event):
        self.clientSocket.close()
        event.accept()
        socket.close(self.clientSocket)


# 레디 버튼을 누르면 뜨는 창
class ReadyConfirmationDialog(QDialog):
    playerReadySignal = pyqtSignal(int)

    def __init__(self, parent=None):
        super(ReadyConfirmationDialog, self).__init__(parent)
        self.setWindowTitle('Ready Confirmation')
        self.setMinimumWidth(300)

        # 버튼 설정
        self.button_box = QDialogButtonBox(QDialogButtonBox.Yes | QDialogButtonBox.No, self)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # 레이아웃 설정
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(QLabel('다른 플레이어를 기다릴까요?'))
        self.layout.addWidget(self.button_box)

    # 게임 다른 플레이어를 기다림
    def accept(self):
        super(ReadyConfirmationDialog, self).accept()
        action = DataConverter.player_action.get("PLAYER_READY")
        self.playerReadySignal.emit(action)

    # 다른 플레이어를 기다리지 않음
    def reject(self):
        super(ReadyConfirmationDialog, self).reject()
        action = DataConverter.player_action.get("PLAYER_NOT_WANT")
        self.playerReadySignal.emit(action)


class WaitingDialog(QDialog):
    playerWaitingSignal = pyqtSignal(int)

    def __init__(self, parent=None):
        super(WaitingDialog, self).__init__(parent)
        self.setWindowTitle("대기 중")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        label = QLabel("게임 시작을 기다리는 중입니다...", self)
        layout.addWidget(label)
        self.setLayout(layout)


class InGameThread(QThread):
    cardUpdateSignal = pyqtSignal(DataConverter)
    myTurnSignal = pyqtSignal()
    notMyTurnSignal = pyqtSignal()

    def __init__(self, parent=None, client_socket=None, data=None):
        super(InGameThread, self).__init__(parent)
        self.clientSocket: socket.socket = client_socket
        self.data: DataConverter = DataConverter(data)
        self.clicked_draw_button: bool = False
        self.clicked_bell_button: bool = False

    def update_event(self, clicked_draw_button=False, clicked_bell_button=False):
        self.clicked_draw_button = clicked_draw_button
        self.clicked_bell_button = clicked_bell_button


    def run(self):
        self.clientSocket.sendall(self.data.send("PLAYER_START"))
        print("init send data from server: ", bytes(self.data))
        self.data.recv(self.clientSocket.recv(1024, socket.MSG_WAITALL))
        print("init Received action from server:", self.data)

        while True:

            if self.clicked_bell_button:
                self.data.set_action("PLAYER_BELL")
                self.clientSocket.sendall(bytes(self.data))
                print("send data from server: ", bytes(self.data))
                self.data.recv(self.clientSocket.recv(1024, socket.MSG_WAITALL))
                print("Received action from server:", self.data)
                self.clicked_bell_button = False


            # 플레이어의 턴인 상태면
            if self.data.my_action == self.data.player_action["PLAYER_TURN"]:
                self.myTurnSignal.emit()
                # 데이터의 업데이트를 대기
                if self.clicked_draw_button:
                    self.data.set_action("PLAYER_DRAW")
                    self.clientSocket.sendall(bytes(self.data))
                    print("send data from server: ", bytes(self.data))
                    self.data.recv(self.clientSocket.recv(1024, socket.MSG_WAITALL))
                    print("Received action from server:", self.data)
                    self.clicked_draw_button = False

            # 플레이어가 인게임 상태면
            if self.data.my_action == self.data.player_action["PLAYER_GAMING"]:
                self.data.recv(self.clientSocket.recv(1024, socket.MSG_WAITALL))
                print("Received action from server:", self.data)
                self.cardUpdateSignal.emit(self.data)
                self.notMyTurnSignal.emit()


            QThread.sleep(1000)








if __name__ == '__main__':
    app = QApplication([])
    client = HarigariClient()
    client.show()
    app.exec_()
