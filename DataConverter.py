import json


# 데이터 변환 클래스
class DataConverter:
    fruits: dict[str, int] = {
        "STRAWBERRY": 0,
        "BANANA": 1,
        "LIME": 2,
        "PLUM": 3
    }
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

    def __init__(self, data, form='utf-8'):
        self.stored_dict: dict
        self.stored_bytes: bytes
        self.my_id: int
        self.my_action: int = 0
        self.player_turn: int
        self.card: dict = {}

        if isinstance(data, str):
            self.__convert_to_bytes(data)

        elif isinstance(data, bytes):
            self.__convert_to_dict(data)
            self.__store_first_data()

    def recv(self, data: bytes):
        self.__convert_to_dict(data)
        self.__store_data()

    def send(self, data: str) -> bytes:
        action_value = DataConverter.player_action.get(data)
        if action_value is None:
            print(f"Error: '{data}' is not a valid action.")
        else:
            self.my_action = int(action_value)

        send_data = json.dumps({"player_id": self.my_id, 'player_action': self.my_action})

        self.__convert_to_bytes(send_data)

        return self.stored_bytes

    def __str__(self):
        return json.dumps(self.stored_dict)

    def __bytes__(self):
        return self.stored_bytes

    def __convert_to_dict(self, data: bytes):
        index = data.decode("utf-8").find('\0')
        self.stored_dict = json.loads(data.decode('utf-8')[:index])

    def __convert_to_bytes(self, data: str):
        self.stored_bytes = int.from_bytes(data.encode('utf-8'), 'little').to_bytes(1024, 'little')

    def __store_first_data(self):
        self.my_id = self.stored_dict.get("player_id")
        self.player_turn = self.stored_dict.get("player_turn")
        self.my_action = self.stored_dict.get("player_action")

    def __store_data(self):
        self.player_turn = self.stored_dict.get("player_turn")
        try:
            self.my_action = self.stored_dict.get("player_action")
        except None:
            for player in self.stored_dict.get("players_data"):
                if player.get("player_id") == self.my_id:
                    # 카드 저장
                    self.card = {
                        'card_volume': player["cardDeckOnTable_volume"],
                        'card_type': self.fruits[player["cardDeckOnTable_type"]]
                    }


