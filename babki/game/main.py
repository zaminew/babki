from player import Player
from game import Game


# TODO при запуске скрипта в него передаются параметры игры например 
    # режим игры колличество игроков, ограничение времени на ход, возможность видеть отчеты других, валюта и так далее 
    # TODO режимы игры: у всех одни и те же события или у каждого свое
    #                   события по типам стабильно как в cashgo или полный рандом как в оригинале cashflow
    #                   другие


player_list = [Player("Eugene", 10000, 1000), Player("Eugene", 10000, 1000)]

game = Game(player_list[0])

while True:
    game.generate_event()
    game.play_step()
    input("Press Enter to continue...\n")
