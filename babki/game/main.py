from player import Player
from game import Game

player_list = [Player("Eugene", 10000, 1000), Player("Eugene", 10000, 1000)]

game = Game(player_list[0])

while True:
    game.generate_event()
    game.play_step()
    input("Press Enter to continue...\n")
