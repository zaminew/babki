
import random
import os
from typing import List

from player import Player
from item import *
from card import *
from game_setting import GameSetting
from json_loader import JsonLoader
from action import Action
from typing import Dict
import uuid

current_dir = os.path.dirname(os.path.abspath(__file__))
cards_file_Path = os.path.join(current_dir, 'data/cards.json')

class Game:
    def __init__(self, settings: GameSetting, players : List[Player]):
        self.settings : GameSetting = settings

        self.players : Dict[str, Player] = {}
        self.game_maker_id = ''
        
        self.events_data : List[Item] = []
        self.current_card : Card = None 
        self.current_step = 0
        self.months_passed = 0
        self.is_game_over = False

        self.expense_cards : List[ExpenseCard] = []
        self.stock_cards : List[StockCard] = []
        self.property_cards: List[PropertyCard] = []
        self.business_cards : List[BusinessCard] = []
        self.salary_card : SalaryCard = SalaryCard('Зарплатка', 'долгожданная в кармане')
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

        self.Deck = [self.expense_cards, self.stock_cards, self.property_cards, self.business_cards, [SalaryCard('День зарплаты', 'долгожданная получка у вас в кармане')]]
        # NOTE группы событий для режима с регулярными типами событий. вариант группировать словари или другой вариант ставить тэги 

        print('\033[35m' + f"создана новая игра с параметрами {self.settings.__str__()}" + '\033[0m')

    def add_player(self, uniq_id, name):
        if self.game_maker_id == '':
            self.game_maker_id = uniq_id
        self.players[uniq_id] =  Player(uniq_id, name, 100000, 100)
    
    def all_actions_taken(self) -> bool:
        return all(player.action_taken for player in self.players.values())
    
    def reset_all_actions_taken(self) -> None:
        for player in self.players.values():
            player.reset_turn()
    
    def remaining_players(self) -> list:
        return [player.name for player in self.players.values() if not player.action_taken]


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

    def set_new_card(self) -> Card:           
        if self.current_step == 0:
            self.current_card = random.choice(self.expense_cards)
        elif self.current_step == 1:
            self.current_card = random.choice(self.stock_cards)
        elif self.current_step == 2:
            self.current_card = random.choice(random.choice([self.property_cards, self.business_cards]))
        else:
            self.current_card = self.salary_card
        
        if self.current_step < 3:
            self.current_step += 1
        else:
            self.current_step = 0
            
        return self.current_card

    def print_card_in_console(self, card : Card):
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
            print(color + f"current card : \n{card.get_card_info(self.player)}" + '\033[0m')
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

    def execute_player_action(self, player_id, user_action_data : Dict[str, int]):
        # TODO проверить если игрок уже сходил и использовал карту, то не позволять ходить
        player : Player = self.players.get(player_id)
        if player is None:
            return False, 'You do not have access to this game'
        print(f'---> {user_action_data}')
        action = Action()
        amount = user_action_data.get('amount', 0)
        
        if 'action' in user_action_data:
            if user_action_data['action'] == 'buy':
                action.buy = amount
                result = self.current_card.execute(player, action)
                player.take_turn()
            elif user_action_data['action'] == 'sell':
                action.sell = amount
                result = self.current_card.execute(player, action)
                player.take_turn()
            elif user_action_data['action'] == 'skip':
                action.skip = 1
                result = self.current_card.execute(player, action)
                player.take_turn()
            elif user_action_data['action'] == 'take_loan':
                result = player.loan.take(amount)
            elif user_action_data['action'] == 'repay_loan':
                result = player.loan.repay(amount)  
            else:
                result = False, f'неизвестная команда для исполнения -> {user_action_data["action"]}'
        
        if result:
            print(f'------> {result}')
            if result[0]:
                if action.is_active():
                    pass
                return True, str(result[1])
            else:
                return False, result[1]
        else:
            print(f'------x result не определен')
        
    
    def get_data(self, player_id) -> Dict[str, int]:
        
        player : Player = self.players.get(player_id)
        if player is None:
            return False, 'You do not have access to this game'
        
        
        # TODO проверить сходил или нет. и если сходил то выдавать информацию о сходивших
        if self.all_actions_taken():
            self.reset_all_actions_taken()
            self.set_new_card()
        
        if player.action_taken:
            remaining_players_list = self.remaining_players()
            return {
            'actions': {
                'buy': 0,
                'sell': 0,
                'skip': 0,
                'take_loan': 0,
                'repay_loan': 0,
            },
            'player': {
                'balance': player.balance,
                'loan': player.loan.amount,
                'salary_level': player.salary_level,
                'cash_flow': player.get_cash_flow(),
                'name': player.name,
                'ownership': player.get_assets_info()
            },
            'players': remaining_players_list,
            'card': 'вы сходили'
        }
            
        available_action = self.current_card.get_available_action(player)
        available_action_loan = player.loan.get_available_action()
        #print(available_action)
        data = {
            'actions': {
                'buy': available_action.buy,
                'sell': available_action.sell,
                'skip': available_action.skip,
                'take_loan': available_action_loan.buy,
                'repay_loan': available_action_loan.sell,
            },
            'player': {
                'balance': player.balance,
                'loan': player.loan.amount,
                'salary_level': player.salary_level,
                'cash_flow': player.get_cash_flow(),
                'name': player.name,
                'ownership': player.get_assets_info()
            },
            'card': self.current_card.get_card_info(player)
        }
        print('-> ' + str(data))
        return data

#NOTE в самом событии будет указано что можно делать с этим событием и какие кнопки будут доступны а так же доступное колличество

# NOTE если будут события разного типа на одном шаге то можно попробовтаь написать функцию 
    # которая будет проверять как давно события этого типа генерировались и если давно то повышать вероятность
    # особенно чтобы не было два события подряд maybe