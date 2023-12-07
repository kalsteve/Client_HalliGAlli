import json


# 데이터 변환 클래스
class DataConverter:
    fruits = {
        "STRAWBERRY": 0,
        "BANANA": 1,
        "LIME": 2,
        "PLUM": 3
    }
    player_action = {
        "PLAYER_NULL" : 0,
        "PLAYER_INIT" : 1,
        "PLAYER_READY" : 2,
        "PLAYER_START" : 3,
        "PLAYER_GAMING" : 4,
        "PLAYER_TURN" : 5,
        "PLAYER_LOSE" : 6,
        "PLAYER_WIN" : 7,
        "PLAYER_DRAW" : 8,
        "PLAYER_BELL" : 9,
        "PLAYER_TURN_END" : 10,
        "PLAYER_DENY" : 11,
        "PLAYER_NOT_WANT" : 12
    }

    def __init__(self, data, form='utf-8'):
        if isinstance(data, str):
            decoded_data = int.from_bytes(data.encode(form), 'little').to_bytes(1024, 'little')

            self.stored_data = json.load(decoded_data)
        elif isinstance(data, bytes):
            try:
                index = data.decode("utf-8").find('\0')
                data = data.decode(form)[:index]
                self.stored_data = json.load(data)
            except UnicodeDecodeError:
                print('UnicodeDecodeError')

        self.stored_data = None

    # JSON 데이터를 반환하는 메소드
    def get_json_data(self):
        return self.stored_data

    def __store_first_data(self, data):
        self.my_id = data["player_id"]
        self.my_action = data["player_action"]

    def __store_data(self, data):

       player_list  = data.gey("players", 'Unknown')

       if player_list == 'Unknown':
           print('Unknown player list')

       for player in player_list:
            if player["player_id"] == self.my_id:
                # 카드 저장
                self.card = {'card_volume': player["cardDeckOnTable_volume"]}
                type = player["cardDeckOnTable_type"]
                self.card['card_type'] = self.fruits[type]
            else
                player_list.append({'player_id': player["player_id"], 'player_action': player["player_action"]}))



