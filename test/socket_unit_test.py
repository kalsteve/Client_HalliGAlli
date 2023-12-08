import json
import unittest

from DataConverter import DataConverter


class MyTestCase(unittest.TestCase):
    def test_something(self):
        DataConverter(self.recive_action_test())


    def recive_action_test(self):
        self.dum1 = {"player_id": 1, "player_action": 2}
        return DataConverter(json.dumps(self.dum1).encode('utf-8'))

    def recive_data_test(self):
        self.dum2 = {"player_id": 1, "all_players_data": [ {"player_id": 1, "cardDeckOnTable_volume":2, "cardDeckOnTable_type": 3}, {"player_id": 2, "cardDeckOnTable_volume":2, "cardDeckOnTable_type": 3}, {"player_id": 3, "cardDeckOnTable_volume":2, "cardDeckOnTable_type": 3}]}
        return DataConverter(json.dumps(self.dum2).encode('utf-8'))



if __name__ == '__main__':
    unittest.main()
