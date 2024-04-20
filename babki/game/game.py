
import random
import os
from typing import List

from player import Player
from event import *
from game_setting import GameSettings
from json_loader import JsonLoader


current_dir = os.path.dirname(os.path.abspath(__file__))
events_file_Path = os.path.join(current_dir, 'data/events.json')

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
        self.property_events : List[Event] = []
        self.business_events : List[Event] = []

        self.group_events : List[List[Event]] = []

        # Создать список объектов Event, ExpenseEvent, StockEvent из данных JSON
        data = JsonLoader.load(events_file_Path)       
        
        for item in data["doodads"]:
            self.expence_events.append(ExpenseEvent(item["title"], "", item["cost"], item["costMin"], item["costMax"], item["costStep"], item["child"]))
        for item in data["stocks"]:
            self.stock_events.append(StockEvent(item["symbol"], item["flavor"], item["price"]))
        for item in data["Property"]:
            self.property_events.append(PropertyEvent("недвижимость", item["title"], item["flavorText"], item["cost"], item["mortgage"], item["downPayment"], item["cashFlow"], item["bed"], item["bath"]))
        for item in data["businesses"]:
            self.business_events.append(BusinessEvent("Бизнес", "Покупка/продажа бизнеса", item["title"], item["flavorText"], item["cost"], item["mortgage"], item["downPayment"], item["cashFlow"]))

        # TODO добавь событий

        self.group_events = [self.expence_events, self.stock_events, self.property_events, self.business_events]
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

    def get_new_event(self) -> Event:
        self.current_event = random.choice(random.choice(self.group_events))
        return self.current_event

    def print_event(self, event : Event):
        if event:
            color = '\033[37m'
            if isinstance(event, ExpenseEvent):
                color = '\033[31m'
            elif isinstance(event, StockEvent):
                color = '\033[33m'
            elif isinstance(event, PropertyEvent):
                color = '\033[36m'
            elif isinstance(event, BusinessEvent):
                color = '\033[34m'
            print(f"\033[31m баланс игрока : {self.player.balance}" + '\033[0m')
            print(color + f"current event : \n{event.get_event_info()}" + '\033[0m')

            actions = event.get_actions(self.player)
            if actions:
                act_str = ''
                if actions.buy: 
                    act_str += '(1)\033[32m купить ' + '\033[0m' + str(actions.buy_amount) + ' макс '
                if actions.sell:
                    act_str += '\033[35m' + '(2)\033[31m продать ' + '\033[0m' + str(actions.sell_amount) + ' макс '
                if actions.check:
                    act_str += '\033[35m' + '(3)\033[33m пропустить ' + '\033[0m'

                print('\033[35m' + f"доступные действия : " + act_str + '\033[0m')
            else:
                print('\033[31m' + f"нет доступных действий : \033[0m")

    def play_step(self, ch):
        event_action = self.current_event.get_actions(self.player)
        player_action = Action(False, 0, False, 0, False)
        act = False
        if ch == '1':
            act = True
            if event_action.buy:
                player_action.buy = True
                print("покупка " + self.current_event.name)
            else:
                print("вы не можете купить " + self.current_event.name)
        elif ch == '2':
            act = True
            if event_action.sell:
                player_action.sell = True
                print("продажа " + self.current_event.name)
            else:
                print("вы не можете продать " + self.current_event.name)
        elif ch == '3':
            act = True
            player_action.check = True
            print("пропуск ")
        elif ch == '4':
            #print(self.player.get_assets_value())
            print(self.player.get_assets_info())

        
        if act and self.current_event.execute_action(player_action, self.player):
            print(" ...успешно... ")
            self.print_event(self.get_new_event())



    def play_month(self):
        event = random.choice(self.events_data)
        act = event.get_actions(self.player)
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