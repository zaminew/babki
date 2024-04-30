
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

        self.expense_cards : List[ExpenseCard] = []
        self.stock_cards : List[StockCard] = []
        self.property_cards: List[PropertyCard] = []
        self.business_cards : List[BusinessCard] = []

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
        if ch == 'BUY':
            act = Action.BUY
        elif ch == 'SELL':
            act = Action.SELL
        elif ch == 'SKIP':
            act = Action.SKIP
        elif ch == 'CHECK':
            #print(self.player.get_assets_value())
            print(self.player.get_assets_info())

        if act:
            res = self.current_card.execute(self.player, act, 1)
            print("-------------------->" + str(res))
            if res[0]:
                print(res[1])
                self.print_event(self.get_new_card())
            else:
                print(res[1])
        
        allow = self.current_card.get_available_actions(self.player)
        
        return {
            'actions': {
                'buy': True if Action.BUY in allow else False,
                'sell': True if Action.SELL in allow else False,
                'skip': True if Action.SKIP in allow else False
            },
            'player': {
                'balance': self.player.balance,
                'salary_level': self.player.salary_level,
                'name': self.player.name,
                'stocks': self.player.get_assets_info()
            },
            'card': self.current_card.get_card_info(),
            "label_text_left": f"{'BUY' if Action.BUY in allow else 'NON'}: {random.randint(1, 100)}",
            "label_text_center": f"{'SELL' if Action.SELL in allow else 'NON'}: {random.randint(1, 100)}",
            "label_text_right": f"{'SKIP' if Action.SKIP in allow else 'NON'}: {random.randint(1, 100)}"
        }

#NOTE в самом событии будет указано что можно делать с этим событием и какие кнопки будут доступны а так же доступное колличество

# NOTE если будут события разного типа на одном шаге то можно попробовтаь написать функцию 
    # которая будет проверять как давно события этого типа генерировались и если давно то повышать вероятность
    # особенно чтобы не было два события подряд maybe