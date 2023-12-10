import json


# 데이터 변환 클래스
class DataConverter:
    # 과일 종류 딕셔너리
    fruits: dict[str, int] = {
        "STRAWBERRY": 0,
        "BANANA": 1,
        "LIME": 2,
        "PLUM": 3
    }
    # 플레이어 액션 딕셔너리
    player_action: dict[str, int] = {
        "PLAYER_NULL": 0,
        "PLAYER_INIT": 1,
        "PLAYER_READY": 2,
        "PLAYER_START": 3,
        "PLAYER_GAMING": 4,
        "PLAYER_TURN": 5,
        "PLAYER_LOSE": 6,
        "PLAYER_WIN": 7,
        "PLAYER_DRAW": 8,
        "PLAYER_BELL": 9,
        "PLAYER_TURN_END": 10,
        "PLAYER_DENY": 11,
        "PLAYER_NOT_WANT": 12
    }

    # 생성자
    def __init__(self, data, form='utf-8'):
        self.stored_dict: dict                          # 수신된 데이터 저장
        self.stored_bytes: bytes                        # 송신할 데이터 저장
        self.my_id: int                                 # 플레이어의 아이디 저장
        self.my_action: int = 0                         # 플레이어의 액션 저장
        self.player_turn: int                           # 플레이어의 턴 저장
        self.card: dict = {'type': int, 'volume': int}  # 플레이어의 카드 저장
        self.player_list: list = []                     # 모든 플레이어의 데이터 저장

        # 데이터 타입이 str인 경우 데이터 저장
        if isinstance(data, str):
            self.stored_dict = json.loads(data)
            self.__convert_to_bytes(data)
        # 데이터 타입이 bytes인 경우 데이터 저장
        elif isinstance(data, bytes):
            self.stored_bytes = data
            self.__convert_to_dict(data)
            self.__store_first_data()

    # 데이터 수신
    def recv(self, data: bytes):
        self.__convert_to_dict(data)
        self.__store_data()

    # 데이터 송신
    def send(self, data: str) -> bytes:
        action_value = DataConverter.player_action.get(data)
        # 보내는 데이터
        send_data = {"player_id": self.my_id, 'player_action': action_value}

        self.__convert_to_bytes(json.dumps(send_data))
        # 플레이어 액션에 따라 데이터 변환
        return self.stored_bytes

    # 데이터 출력이 str일 경우
    def __str__(self):
        return json.dumps(self.stored_dict)

    # 데이터 출력이 bytes일 경우
    def __bytes__(self):
        return self.stored_bytes

    # 수신된 데이터에 쓰레기값이 붙음으로 쓰레기값 제거 후 딕셔너리로 변경
    def __convert_to_dict(self, data: bytes):
        index = data.decode("utf-8").find('\0')
        self.stored_dict = json.loads(data.decode('utf-8')[:index])

    # 보낼 데이터를 bytes로 변경, c언어에서는 1024바이트로 고정 되어있음으로 1024바이트로 변경
    def __convert_to_bytes(self, data: str):
        self.stored_bytes = int.from_bytes(data.encode('utf-8'), 'little').to_bytes(1024, 'little')

    # 처음 데이터를 받았을 때 저장
    def __store_first_data(self):
        self.my_id = self.stored_dict.get("player_id")
        self.player_turn = self.stored_dict.get("player_turn")
        self.my_action = self.stored_dict.get("player_action")

    # 데이터를 받았을 때 마다 저장
    def __store_data(self):
        self.player_turn = self.stored_dict.get("player_turn")
        # 플레이어의 액션을 받았을 때
        if(self.stored_dict.get("player_action") is not None):
            self.my_action = self.stored_dict.get("player_action")
        # 플레이어의 카드를 받았을 때, 액션이 없는 경우 데이터를 수신한다고 생각하고 저장된다.
        else:
            self.player_list = []
            for player in self.stored_dict.get("all_players_data"):
                # 플레이어의 데이터 전체 저장
                self.player_list.append({
                    'player_id': player["player_id"],
                    'card': {
                        # 과일 종류를 숫자에서 문자로 저장
                        'type': {value: key for key, value in self.fruits.items()}[player["cardDeckOnTable_type"]],
                        'volume': player["cardDeckOnTable_volume"]
                    }
                })
                # 플레이어의 아이디가 나의 아이디와 같을 때, 내 카드 데이터 저장
                if player.get("player_id") == self.my_id:
                    # 카드 저장
                    self.card = {
                        'type': {value: key for key, value in self.fruits.items()}[player["cardDeckOnTable_type"]],
                        'volume': player["cardDeckOnTable_volume"]
                    }

    # 플레이어의 아이디를 가져옴
    def get_id(self) -> int:
        return self.my_id

    # 액션을 가져옴
    def get_action(self) -> str:
        return {value: key for key, value in self.player_action.items()}[self.my_action]

    # 턴을 가져옴
    def get_turn(self) -> int:
        return self.player_turn

    # 나의 카드를 가져옴
    def get_card_my(self) -> dict:
        return self.card

    # 플레이어의 아이디로 플레이어의 카드를 가져옴
    def get_card_by_id(self, id) -> dict:
        for player in self.player_list:
            if player.get('player_id') == id:
                return player.get('card')

    # 플레이어의 아이디로 플레이어의 데이터를 가져옴
    def get_player_by_id(self, player_id: int) -> dict:
        for player in self.player_list:
            if player.get('player_id') == player_id:
                return player

    # 플레이어의 데이터를 가져옴
    def get_player_list(self) -> list:
        return self.player_list

    def set_action(self, action: int):
        self.my_action = action
        # 보내는 데이터
        send_data = {"player_id": self.my_id, 'player_action': self.my_action}
        self.__convert_to_bytes(json.dumps(send_data))

