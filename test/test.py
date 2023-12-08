import json
import socket
from DataConverter import DataConverter

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('172.19.215.16', 4892))
print("Connected to server")

while True:
    # 서버로부터 메시지를 수신
    data = client_socket.recv(1024, socket.MSG_WAITALL)

    print(DataConverter(data))
    recvJson = DataConverter(data)
    print(recvJson)

    # if(int(recvMessage["player_action"]) == 5):
    #     print("player_turn")
    #     data = DataConverter(client_socket.recv(1024, socket.MSG_WAITALL))
    #     recvMessage = data.get_str()
    #     print(recvMessage)

    # 서버에 메시지를 전송
    sendMessage = int(input("send-> "))
    if sendMessage == "exit":
        break

    bytesString = DataConverter({"player_id": id, "player_action": sendMessage}, 'utf-8')
    print(bytesString)
    client_socket.sendall(bytesString)

client_socket.close()


