import json
import unittest

from DataConverter import DataConverter


class MyTestCase(unittest.TestCase):
    dum1 = {"player_id": 1, "player_action": 2}
    dum2 = {"player_id": 1,
            "all_players_data": [{"player_id": 1, "cardDeckOnTable_volume": 2, "cardDeckOnTable_type": 3},
                                 {"player_id": 2, "cardDeckOnTable_volume": 2, "cardDeckOnTable_type": 3},
                                 {"player_id": 3, "cardDeckOnTable_volume": 2, "cardDeckOnTable_type": 3}]}

    def test_something(self):
        DataConverter(self.receive_action_test())

    def test_convert(self):
        data = DataConverter(self.dum1)

        data.send({value: key for key, value in DataConverter.player_action.items()}[12])

        self.assertEqual(data.my_action, data.player_action["PLAYER_NOT_WANT"])

    def receive_action_test(self):
        return DataConverter(json.dumps(self.dum1).encode('utf-8'))

    def receive_data_test(self):
        return DataConverter(json.dumps(self.dum2).encode('utf-8'))



if __name__ == '__main__':
    unittest.main()
