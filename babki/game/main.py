from player import Player
from game import Game, GameSettings


# TODO при запуске скрипта в него передаются параметры игры например 
    # режим игры колличество игроков, ограничение времени на ход, возможность видеть отчеты других, валюта, сумма или поток для победы и так далее 
   # NOTE режимы игры: у всех одни и те же события или у каждого свое
    #                   события по типам стабильно как в cashgo или полный рандом как в оригинале cashflow
    #                   другие
# TODO в конце игры выводится статистика игры и игроков, возможно графики, рискованные шаги количество сделок, типы и так далее

# NOTE  features  


player_list = [Player("Eugene", 10000, 1000), Player("Eugene", 10000, 1000)]

game_settings = GameSettings("fast", 6, "hard", "one_for_all", "stable_events", True)

game = Game(game_settings, player_list)

game.start()

while True:
    game.play_step(game.get_event())
    input("Press Enter to continue...\n")
