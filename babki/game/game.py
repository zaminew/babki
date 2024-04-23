
import random
import os
from typing import List

from player import Player
from item import *
from card import *
from game_setting import GameSettings
from json_loader import JsonLoader
from action import Action

current_dir = os.path.dirname(os.path.abspath(__file__))
cards_file_Path = os.path.join(current_dir, 'data/cards.json')

class Game:
    def __init__(self, settings: GameSettings, players : List[Player]):
       
        self.settings : GameSettings = settings

        self.players : List[Player] = players
        # FIXME v временное поле
        self.player : Player = players[0]
        self.events_data : List[Item] = []
        self.current_card : Card = None 
        self.current_step = 0
        self.months_passed = 0
        self.is_game_over = False

        self.expense_cards : List[Card] = []
        self.stock_cards : List[Card] = []
        self.property_cards: List[Card] = []
        self.business_cards : List[Card] = []

        self.Deck : List[List[Card]] = []

        # Создать список объектов Event, ExpenseEvent, StockEvent из данных JSON
        data = JsonLoader.load(cards_file_Path)       
        
        for card in data["expense_cards"]:
            self.expense_cards.append(ExpenseCard(card['title'], card['description'], card['price'], card['child']))

        for card in data["stock_cards"]:
            item_data = card["item"]
            item = StockItem(item_data["name"], item_data["price"], item_data["quantity"])
            self.stock_cards.append(StockCard(card['title'], card['description'], item))

        for card in data["property_cards"]:
            item_data = card["item"]
            item = PropertyItem(item_data["name"], item_data["price"], item_data["mortgage"], item_data["down_payment"], item_data["cash_flow"], item_data["bed"], item_data["bath"])
            self.property_cards.append(PropertyCard(card['title'], card['description'], item))

        for card in data["business_cards"]:
            item_data = card["item"]
            item = BusinessItem(item_data["name"], item_data["price"], item_data["mortgage"], item_data["down_payment"], item_data["cash_flow"])
            self.business_cards.append(BusinessCard(card['title'], card['description'], item))

        # TODO добавь событий

        self.Deck = [self.expense_cards, self.stock_cards, self.property_cards, self.business_cards]
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

    def get_new_card(self) -> Card:
        self.current_card = random.choice(random.choice(self.Deck))
        return self.current_card

    def print_event(self, card : Card):
        if card:
            color = '\033[37m'
            if isinstance(card, ExpenseCard):
                color = '\033[31m'
            elif isinstance(card, StockCard):
                color = '\033[33m'
            elif isinstance(card, PropertyCard):
                color = '\033[36m'
            elif isinstance(card, BusinessCard):
                color = '\033[34m'
            print(f"\033[31m баланс игрока : {self.player.balance}" + '\033[0m')
            print(color + f"current card : \n{card.get_card_info()}" + '\033[0m')
            '''
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
            '''
    def play_step(self, ch):
        act : Action = None
        if ch == '1':
            act = Action.BUY
            amount = int(input('количество для покупки -> '))
        elif ch == '2':
            act = Action.SELL
            amount = int(input('количество для продажи -> '))
        elif ch == '3':
            act = Action.CHECK
            amount = 1
        elif ch == '4':
            #print(self.player.get_assets_value())
            print(self.player.get_assets_info())

        if act:
            strategy = StrategyFactory.get_strategy(act, self.current_card)
            res = strategy.execute(self.player, self.current_card, amount)
            if res[0]:
                print(res[1])
                self.print_event(self.get_new_card())
            else:
                print(res[1])


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