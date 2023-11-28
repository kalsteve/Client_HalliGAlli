import socket
import json

# 소켓 객체 생성
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 서버에 접속
client_socket.connect(('localhost', 12345))

# 서버로부터 데이터를 수신
data = client_socket.recv(1024)

# JSON 형식의 문자열을 파이썬 객체로 변환
cards = json.loads(data.decode())

# 연결 종료
client_socket.close()


