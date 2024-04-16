from action import Action
from player import Player

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