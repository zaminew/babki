from player import Player
from game import Game
from game_setting import GameSettings, Speed, Difficulty, GameType, GameMode

# TODO при запуске скрипта в него передаются параметры игры например 
    # режим игры колличество игроков, ограничение времени на ход, возможность видеть отчеты других, валюта, сумма или поток для победы и так далее 
   # NOTE режимы игры: у всех одни и те же события или у каждого свое
    #                   события по типам стабильно как в cashgo или полный рандом как в оригинале cashflow
    #                   другие
# TODO в конце игры выводится статистика игры и игроков, возможно графики, рискованные шаги количество сделок, типы и так далее

# NOTE  features  добавить казино для любителей порисковать

# TODO добиться того чтобы игра отдавала данные в виде json и в них же были доступные действия и ограничения
    # сначала можно передавать в игру параметры запуска 
    # игра отвечает тем что она успешно была создана и что находится в стадии брифинга.
    # когда все игроки нашлись, вошли и подтвердили готовность игра переходит в активную стадию и передает всем 
        # информацю о первом событии вместе с доступными действиями
    # ждет пока все игроки не передадут информацию об активности. кроме основной активности, 
        # игра может принимать запросы на исполнение промежуточных активносте типа взять/погасить кредит и т. п.
    # в конце хода когда все сделали свои действия проверяются условия для победы, и если победы нет, то генерируется новое событие.
    # попробовать переписать режимы игры и типы игры по паттерну стратегия
    # Аукционы для покупки некоторых событий
    # и в целом взаимодействия между игроками
    # например продажа акций сначала игрокам, как в монополии в случае банкротства
    # события влияющие на всех например, ввели льготную программу на ипотеку - денежный поток с квартир снизился
    # вышел закон об обязательном фискальном аппарате, заплатите еще 1000 рублей и денежный потом - 1%



player_list = [Player("Eugene", 10000, 1000), Player("Eugene", 10000, 1000)]

game_settings = GameSettings(6, Speed.NORMAL, Difficulty.MEDIUM, GameType.ONE_FOR_ALL, GameMode.STABLE_EVENTS, True)

game = Game(game_settings, player_list)

#game.start()
game.print_event(game.get_new_card())
ch = None
while True:
    game.play_step(ch)
    ch = input("Press Enter to continue...\n")
