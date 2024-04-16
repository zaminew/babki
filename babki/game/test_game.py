import unittest

from player import Player
from game import Game, GameSettings

class TestGame(unittest.TestCase):
    def test_create_game(self):

        player_list = [Player("Eugene", 10000, 1000), Player("Eugene", 10000, 1000)]
        game_settings = GameSettings("fast", 6, "hard", "one_for_all", "stable_events", True)
        game = Game(game_settings, player_list)

        self.assertEqual(len(game.players), 2)
        

    def test_settings_game(self):
        player_list = [Player("Eugene", 10000, 1000), Player("Eugene", 10000, 1000)]
        game_settings = GameSettings("fast", 6, "hard", "one_for_all", "stable_events", True)
        game = Game(game_settings, player_list)

        self.assertEqual(game.settings.difficulty, 'hard')
        self.assertEqual(game.settings.num_players, 6)

if __name__ == '__main__':
    unittest.main()