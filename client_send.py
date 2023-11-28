import socket
import json

# 소켓 객체 생성
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 서버에 접속
client_socket.connect(('localhost', 12345))

# 파이썬 객체를 JSON 형식의 문자열로 변환
data = json.dumps({'key': 'value'})

# 서버로 데이터를 전송
client_socket.sendall(data.encode())

# 연결 종료
client_socket.close()
