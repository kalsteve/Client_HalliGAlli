# client.py
import socket
import json
import threading

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QMessageBox, \
    QGridLayout, QFrame
from PyQt5.QtCore import Qt, QTimer


class HarigariClient(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initMainMenu()

        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect(('220.149.128.100', 4061))

        self.card_labels = [QLabel(self) for _ in range(4)]

        self.turn_label = QLabel(self)
        self.turn_label.setAlignment(Qt.AlignCenter)
        self.turn_label.setStyleSheet("color: white; font-size: 18px;")

        """self.timer = QTimer(self)
        self.timer.timeout.connect(self.sendSignalToServer)
        self.timer.start(10)  # Set the timeout interval to 5000 milliseconds (5 seconds)
"""

    def sendSignalToServer(self):
        # Send a signal to the server (you may customize this signal)
        signal_data = {'action': 'client_signal'}
        self.clientSocket.send(json.dumps(signal_data).encode())
        print("Signal sent to server")

    def receive_data(self):
        while True:
            try:
                data = self.clientSocket.recv(1024).decode()
                if not data:
                    # Connection closed by the server
                    break
                print(f"Received data from server: {data}")
                card_info = json.loads(data)
                current_player = card_info.get('current_player')
                cards = card_info.get('cards')

                if current_player is not None and cards is not None:
                    print(f"Received card information for Player {current_player}: {cards}")

                    if 'action' in card_info:
                        action = card_info['action']
                        if action == 'bell_pressed':
                            self.handleBellPress()
                        elif action == 'card_transfer':
                            self.handleCardTransfer()

                    # Update card labels based on received cards
                    for i, card_label in enumerate(self.card_labels):
                        card_image_path = f'images/{cards[i]}.jpg'
                        card_label.setPixmap(QPixmap(card_image_path))

                    # Update turn label
                    self.turn_label.setText(f"Current Turn: {current_player}")


            except Exception as e:
                print(f"Error in receive_data: {e}")
                break

    def initMainMenu(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        image_label = QLabel(self)
        image_label.setPixmap(QPixmap('images/title.png'))  # Replace with the actual path to your image
        image_label.setAlignment(Qt.AlignCenter)  # Center the image
        image_label.setScaledContents(True)

        self.game_start_button = QPushButton('Game Start', self)
        self.game_start_button.clicked.connect(self.showGameScreen)

        layout = QVBoxLayout(self.central_widget)
        layout.addWidget(image_label)
        layout.addWidget(self.game_start_button)

        self.setWindowTitle('Halli Galli')
        self.setFixedSize(600, 800)

    def initGameScreen(self):
        self.receive_thread = threading.Thread(target=self.receive_data)
        self.receive_thread.start()

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
        bell_button = QPushButton('Ring Bell', self)
        bell_button.clicked.connect(self.sendBellAction)
        bell_button.setStyleSheet("background-color: white;")

        # Create draw card button
        draw_card_button = QPushButton('Draw Card', self)
        draw_card_button.clicked.connect(self.drawCardAction)
        draw_card_button.setStyleSheet("background-color: white;")

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
        layout.addWidget(bell_button, 6, 0, 1, 2)  # Row 6, Column 0, Span 1 row, 2 columns

        # Add draw card button
        layout.addWidget(draw_card_button, 6, 2, 1, 2)  # Row 6, Column 2, Span 1 row, 2 columns

        self.setWindowTitle('Halli Galli')
        self.setFixedSize(600, 800)  # Set fixed size for the window
        self.show()

    def drawCardAction(self):
        action_data = {'player_number': 1, 'action': 'draw'}
        self.clientSocket.send(json.dumps(action_data).encode())
        print("Draw Card pressed!")

    def sendBellAction(self):
        action_data = {'player_number': 1, 'action': 'bell'}
        self.clientSocket.send(json.dumps(action_data).encode())
        print("Bell pressed!")

    def handleBellPress(self):
        print("Bell pressed!")

    def handleCardTransfer(self):
        print("Card transfer initiated!")

    def showGameScreen(self):
        self.initGameScreen()
        self.show()

    def closeEvent(self, event):
        self.clientSocket.close()
        event.accept()
        socket.close()


if __name__ == '__main__':
    app = QApplication([])
    client = HarigariClient()
    client.show()
    app.exec_()
