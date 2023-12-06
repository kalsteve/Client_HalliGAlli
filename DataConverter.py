import json


# 데이터 변환 클래스
class DataConverter:
    def __init__(self, data, form='utf-8'):
        if isinstance(data, str):
            decoded_data = int.from_bytes(data.encode(form), 'little').to_bytes(1024, 'little')
            self.data = decoded_data
        elif isinstance(data, bytes):
            try:
                encoded_data = data.decode(form).split('\0')[0]
                self.data = json.loads(encoded_data)
            except UnicodeDecodeError:
                print('UnicodeDecodeError')

    # json 데이터 형식인 경우만 출력
    def __str__(self):
        return json.dumps(self.data)

    # bytes 데이터 형식인 경우만 출력
    def __bytes__(self):
        return self.data