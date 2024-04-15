
import random
import os
from typing import List

from player import Player
from event import *
from json_loader import JsonLoader

# Получаем путь к текущему файлу
current_dir = os.path.dirname(os.path.abspath(__file__))

# Формируем путь к файлу 'doodads.json'
events_file_Path = os.path.join(current_dir, 'data/events.json')


class Game:
    def __init__(self, player : Player):
        self.player : Player = player
        self.events_data : List[Event] = []
        self.current_event : Event = None
        self.current_step = 0
        self.months_passed = 0

        self.expence_events : List[Event] = []
        self.stock_events : List[Event] = []

        self.group_events : List[List[Event]] = []

        # Создать список объектов Event, ExpenseEvent, StockEvent из данных JSON
        data = JsonLoader.load(events_file_Path)       
        
        for item in data["doodads"]:
            self.expence_events.append(ExpenseEvent("Непредвиденные расходы", "Снова траты", item["title"], item["cost"], item["costMin"], item["costMax"], item["costStep"], item["child"]))
        for item in data["stocks"]:
            self.stock_events.append(StockEvent("Фондовый рынок", "купи/продай", item["symbol"], item["price"], item["flavor"]))

        self.group_events = [self.expence_events, self.stock_events]

        '''
        for item in data["homes"]:
            self.events_data.append(Event(item["title"], item["flavorText"]))
        for item in data["doodads"]:
            self.events_data.append(ExpenseEvent("Непредвиденные расходы", "Снова траты", item["title"], item["cost"], item["costMin"], item["costMax"], item["costStep"], item["child"]))
        for item in data["stocks"]:
            self.events_data.append(StockEvent("Фондовый рынок", "купи/продай", item["symbol"], item["price"], item["flavor"]))
        '''


    def generate_event(self):
        #self.current_event = random.choice(self.events_data)
        self.current_event = random.choice(random.choice(self.group_events))

    def play_step(self):
        if self.current_event:
            print(f"current event : \n{self.current_event.get_event_info()}")
        

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
        

#TODO в самом событии будет указано что можно делать с этим событием и какие кнопки будут доступны а так же доступное колличество





#TODO если будут события разного типа на одном шаге то можно попробовтаь написать функцию 
    # которая будет проверять как давно события этого типа генерировались и если давно то повышать вероятность

