import unittest

from player import Player
from game import Game
from game_setting import GameSetting, Speed, Difficulty, GameType, GameMode

class TestGame(unittest.TestCase):
    def test_create_game(self):
        
        player_list = [Player("Eugene", 10000, 1000), Player("Eugene", 10000, 1000)]
        game_settings = GameSetting(2, "normal", "medium", "one_for_all", "stable_events", True)
        game = Game(game_settings, player_list)

        self.assertEqual(len(game.players), 2)
        
    def test_create_settings_from_json(self):
        json_data_example = '''
        { 
            "num_players": 4,
            "speed": "normal",
            "difficulty": "medium",
            "game_type": "one_for_all",
            "game_mode": "stable_events",
            "hide_stats": true
        }
        '''

        json_expect = '{"num_players": 4, "speed": "normal", "difficulty": "medium", "game_type": "one_for_all", "game_mode": "stable_events", "show_stats": true}'

        game_settings = GameSetting.from_json(json_data_example)

        self.assertEqual(str(game_settings), json_expect)


    def test_settings_game(self):
        player_list = [Player("Eugene", 10000, 1000), Player("Eugene", 10000, 1000)]
        game_settings = GameSetting(6, Speed.NORMAL, Difficulty.MEDIUM, GameType.ONE_FOR_ALL, GameMode.STABLE_EVENTS, True)
        game = Game(game_settings, player_list)

        self.assertEqual(game.settings.difficulty, Difficulty.MEDIUM)
        self.assertEqual(game.settings.num_players, 6)

if __name__ == '__main__':
    unittest.main()