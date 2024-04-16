
import random
import os
from typing import List

from player import Player
from event import *
import json
from json_loader import JsonLoader

# Получаем путь к текущему файлу
current_dir = os.path.dirname(os.path.abspath(__file__))

# Формируем путь к файлу 'doodads.json'
events_file_Path = os.path.join(current_dir, 'data/events.json')

class GameSettings:
    def __init__(self, speed, num_players, difficulty, game_type, game_mode, hide_stats):
        self.speed = speed
        self.num_players = num_players
        self.difficulty = difficulty
        self.game_type = game_type
        self.game_mode = game_mode
        self.hide_stats = hide_stats

    @classmethod
    def from_json(cls, json_str):
        json_data = json.loads(json_str)
        return cls(**json_data)        
    
    def to_json(self):
        return {
            "speed": self.speed,
            "num_players": self.num_players,
            "difficulty": self.difficulty,
            "game_type": self.game_type,
            "game_mode": self.game_mode,
            "hide_stats": self.hide_stats
        }

    def __str__(self):
        return json.dumps(self.to_json())


class Game:
    def __init__(self, settings: GameSettings, players : List[Player]):
       
        self.settings : GameSettings = settings

        self.players : List[Player] = players
        # FIXME v временное поле
        self.player : Player = players[0]
        self.events_data : List[Event] = []
        self.current_event : Event = None # FIXME still needed?
        self.current_step = 0
        self.months_passed = 0
        self.is_game_over = False

        self.expence_events : List[Event] = []
        self.stock_events : List[Event] = []

        self.group_events : List[List[Event]] = []

        # Создать список объектов Event, ExpenseEvent, StockEvent из данных JSON
        data = JsonLoader.load(events_file_Path)       
        
        for item in data["doodads"]:
            self.expence_events.append(ExpenseEvent("Непредвиденные расходы", "Снова траты", item["title"], item["cost"], item["costMin"], item["costMax"], item["costStep"], item["child"]))
        for item in data["stocks"]:
            self.stock_events.append(StockEvent("Фондовый рынок", "купи/продай", item["symbol"], item["price"], item["flavor"]))
        # TODO добавь событий

        self.group_events = [self.expence_events, self.stock_events]
        # NOTE группы событий для режима с регулярными типами событий. вариант группировать словари или другой вариант ставить тэги 

        print('\033[35m' + f"создана новая игра с параметрами {self.settings.__str__()}" + '\033[0m')

    def start(self):

        while not all(player.is_ready for player in self.players):
            char = input('Подтвердите готовность - введите y или r ').lower()
            if char == 'y' or char == 'r': 
                print('\033[35m' + 'игра началась' + '\033[0m')
                break
            
            # TODO добавить логику ожидания входа или готовности игроков

    def end_game(self):
        self.is_game_over = True
        # TODO логика вывода статистики и завершения игры

    def get_event(self) -> Event:
        #self.current_event = random.choice(self.events_data)
        return random.choice(random.choice(self.group_events))

    def play_step(self, event : Event):
        if event:
            color = '\033[37m'
            if isinstance(event, ExpenseEvent):
                color = '\033[31m'
            elif isinstance(event, StockEvent):
                color = '\033[36m'

            print(color + f"current event : \n{event.get_event_info()}" + '\033[0m')
        

    def play_month(self):
        event = random.choice(self.events_data)
        act = event.get_action(self.player)
        print(f"name {event.name}")
        if act.buy:
            print(" BUY ")
            print(act.buy_amount)
        if act.sell:
            print(" SELL ")
            print(act.sell_amount)
        if act.check:
            print(" CHECK ")

        
        event.execute_action(self.player, Action(False, 0, False, 0, True))
        if event.input_requires:
            print("")
        self.current_step += 1
        
        print(f"Step: {self.current_step}")
        if self.current_step % 4 == 0:
            print("PAYDAY")
            self.player.balance += self.player.salary_level
        print(f"Balance: {self.player.balance}")
        

#NOTE в самом событии будет указано что можно делать с этим событием и какие кнопки будут доступны а так же доступное колличество

# NOTE если будут события разного типа на одном шаге то можно попробовтаь написать функцию 
    # которая будет проверять как давно события этого типа генерировались и если давно то повышать вероятность


if __name__ == "__main__":
    game_settings = GameSettings("fast", 3, "hard", "one_for_one", "random_event", True)
    print(game_settings)