import json
import socket
import threading

from DataConverter import DataConverter

buffer_size = 256

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('220.149.128.100', 4101))
print("Connected to server")

data = DataConverter(client_socket.recv(buffer_size, socket.MSG_WAITALL))
print(data)

# 서버에 메시지를 전송
sendMessage = int(input("send-> "))
data.send({value: key for key, value in DataConverter.player_action.items()}[sendMessage])
print(bytes(data))
client_socket.sendall(bytes(data))

data.recv(client_socket.recv(buffer_size, socket.MSG_WAITALL))
print("\n", data)

while True:

    if data.my_action == data.player_action["PLAYER_GAMING"]:
        lock = threading.Lock()
        # 정보를 받아오는 쓰레드 생성
        thread = threading.Thread(target=lambda : data.recv(client_socket.recv(buffer_size)))
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
        # 서버에 메시지를 전송
        sendMessage = int(input("send-> "))
        data.send({value: key for key, value in DataConverter.player_action.items()}[sendMessage])
        print(bytes(data))

        client_socket.sendall(bytes(data))

        data.recv(client_socket.recv(buffer_size, socket.MSG_WAITALL))
        print("\n", data)

        print("player_turn")

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