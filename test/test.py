import json
import socket
import threading

from DataConverter import DataConverter



client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('172.23.202.241', 4892))
print("Connected to server")

data = DataConverter(client_socket.recv(1024, socket.MSG_WAITALL))
print(data)

# 서버에 메시지를 전송
sendMessage = int(input("send-> "))

data.send({value: key for key, value in DataConverter.player_action.items()}[sendMessage])
print(bytes(data))
client_socket.sendall(bytes(data))

data.recv(client_socket.recv(1024, socket.MSG_WAITALL))

while True:


    if data.my_action == data.player_action["PLAYER_GAMING"]:
        lock = threading.Lock()
        # 정보를 받아오는 쓰레드 생성
        thread = threading.Thread(target=lambda : data.recv(client_socket.recv(1024)))
        data.recv(client_socket.recv(1024, socket.MSG_WAITALL))

        print("player_gaming")

        sendMessage = int(input("send-> "))
        if sendMessage == "exit":
            break


        bytesString = data.send({value: key for key, value in DataConverter.player_action.items()}[sendMessage])
        lock.acquire()
        client_socket.sendall(bytesString)
        lock.release()

        # 카드 정보를 받아옴
        continue

    if data.my_action == data.player_action["PLAYER_TURN"]:
        data.recv(client_socket.recv(1024, socket.MSG_WAITALL))

        print("player_turn")

        sendMessage = int(input("send-> "))
        if sendMessage == "exit":
            break

        data.send({value: key for key, value in DataConverter.player_action.items()}[sendMessage])
        client_socket.sendall(bytes(data))

        # 카드 정보를 받아옴
        continue



client_socket.close()

# 서버에 메시지를 전송
# sendMessage = int(input("send-> "))
# if sendMessage == "exit":
#     break
#
# data.send({value: key for key, value in DataConverter.player_action.items()}[sendMessage])
# print(bytes(data))
# client_socket.sendall(bytes(data))