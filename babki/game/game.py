import json
import random
import os
from typing import List

# Получаем путь к текущему файлу
current_dir = os.path.dirname(os.path.abspath(__file__))

# Формируем путь к файлу 'doodads.json'
events_file_Path = os.path.join(current_dir, 'data/events.json')
doodads_file_path = os.path.join(current_dir, 'data/doodads.json')

class Player:
    def __init__(self, name, balance, salary_level):
        self.name = name
        self.balance = balance
        self.salary_level = salary_level
        self.credits = 0
        self.child = False

    def take_credit(self, amount):
        pass

    def repay_credit(self, amount):
        pass

    def calculate_balance(self):
        pass


class Action:
    def __init__(self, buy=False, buy_amount=0, sell=False, sell_amount=0, check=False):
        self.buy = buy
        self.buy_amount = buy_amount
        self.sell = sell
        self.sell_amount = sell_amount
        self.check = check

class JsonLoader:
    @staticmethod
    def load(file_name):
        with open(file_name, 'r') as file:
            return json.load(file)

class Event:
    def __init__(self, name, effect):
        self.name = name
        self.effect = effect
        self.input_requires = False

    def get_action(self, player : Player) -> Action:
        return Action(False, 0, False, 0, True)

    def execute_action(self, player : Player, action : Action) -> bool:
        return True

    def get_event_info(self):
        return f"\tname : {self.name} \n\tdesc : {self.effect}"
        #TODO наследники в результате должны вывести доступные действие с данным событием 
            # а пользователь может применить это действие на событии и получить результат
            # возможно понадобится несколько функций, вывод, ввод, результат. И это для одного шага


class ExpenseEvent(Event):
    def __init__(self, name, effect, title, expense, costMin, costMax, costStep, child):
        super().__init__(name, effect)
        self.title = title
        self.expense = expense
        self.costMin = costMin
        self.costMax = costMax
        self.costStep = costStep
        self.child = child

    def get_action(self, player : Player) -> Action:
        return Action(False, 0, False, 0, True)

    def execute_action(self, player, action : Player):
        cost = self.expense['cost']
        if player.balance >= cost:
            player.balance -= cost
            return True
        return False

    def get_event_info(self):
        return f"\tname : {self.name} \n\tdesc : {self.effect} \n\tвы потеряли : {self.expense}"


class StockEvent(Event):
    def __init__(self, name, effect, symbol, price, flavor):
        super().__init__(name, effect)
        self.symbol = symbol
        self.price = price
        self.flavor = flavor

    def get_action(self, player : Player) -> Action:
        act = Action(False, 0, False, 0, True)
        price = self.stock['price']
        if price > player.balance:
            act.buy = True
            act.buy_amount = player.balance // price
        # TODO if player has stock he can sell
        return act

    def execute_action(self, player : Player, action : Action) -> bool:
        price = self.stock['price']
        if action.buy:
            summ = action.buy_amount * price
            player.balance -= summ
            print(f"{self.name}: Покупка -{summ}")
        elif action.sell:
            summ = action.sell_amount * price
            player.balance += summ 
            print(f"{self.name}: Продажа +{summ}")
        elif action.check:
            print(f"{self.name}: Проехали")
        return True
    
    def get_event_info(self):
        return f"\tname : {self.name} \n\tdesc : {self.flavor} \n\tФин инструмент : {self.symbol} по цене {self.price}"


class Game:
    def __init__(self, player, events_data):
        self.player = player
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
        

# Загрузка данных из JSON
events_data : List[Event] = [
    
]

#TODO в самом событии будет указано что можно делать с этим событием и какие кнопки будут доступны а так же доступное колличество


player = Player("Player1", 10000, 1000)

game = Game(player, events_data=events_data)

while True:
    game.generate_event()
    game.play_step()
    input("Press Enter to continue...\n")



#TODO если будут события разного типа на одном шаге то можно попробовтаь написать функцию 
    # которая будет проверять как давно события этого типа генерировались и если давно то повышать вероятность

