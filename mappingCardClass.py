from enum import Enum
from json import JSONEncoder

# json를 Card 객체로 변환
class CardDecoder(Enum, JSONEncoder):
    STRAWBERRY = 0
    BANANA = 1
    LIME = 2
    PLUM = 3

    def __init__(self):
        super().__init__()

    def default(self, o):
        return

    def to_enum(self):
        if self == "STRAWBERRY":
            return CardDecoder.STRAWBERRY
        elif self == "BANANA":
            return CardDecoder.BANANA
        elif self == "LIME":
            return CardDecoder.LIME
        elif self == "PLUM":
            return CardDecoder.PLUM
        else:
            return None

    def to_string(self):
        return self.name

    def decode(self, o):
        return self.decode(o).slpit('\0')[0]

    def encode(self, o):
        return int.from_bytes(self.encode(o), 'little').to_bytes(1024, 'little')

