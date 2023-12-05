from firstWindow import FirstWindow
from secondWindow import SecondWindow
from PyQt5.QtWidgets import QApplication
from socket import *
import socket
import sys

class MyDisplay:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.first_window = FirstWindow(self.client_socket)
        self.window = SecondWindow(self.client_socket)
        self.window.hide()

    def show_window1(self):
        self.first_window.switch_window.connect(self.show_window2)
        self.first_window.show()

    def show_window2(self):
        self.first_window.close()
        self.window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    display = MyDisplay()
    display.show_window1()
    sys.exit(app.exec_())
