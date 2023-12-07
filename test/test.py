import json
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('172.19.215.16', 4892))
print("Connected to server")

while True:
    # 서버로부터 메시지를 수신
    data = client_socket.recv(1024, socket.MSG_WAITALL)
    print(data)
    index = data.decode("utf-8").find('\0')
    print('index : ', index)
    recvMessage = data.decode("utf-8")[:index]
    print(recvMessage)
    # 문자열을 json 형식으로 변환
    recvJson = json.loads(recvMessage)
    id = recvJson["player_id"]
    action = recvJson["player_action"]
    print("player_id : ", id)
    print("player_action : ", action)

    # 서버에 메시지를 전송
    sendMessage = int(input("send-> "))
    if sendMessage == "exit":
        break
    sendJson = json.dumps({"player_id": id, "player_action": sendMessage})
    print(sendJson);
    bytesString = int.from_bytes(sendJson.encode('utf-8'), 'little').to_bytes(1024, 'little')
    print(bytesString);
    client_socket.sendall(bytesString)

client_socket.close()


