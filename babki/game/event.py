from action import Action
from player import Player

class Event:
    def __init__(self, name, effect):
        self.name = name
        self.effect = effect
        self.input_requires = False

    def get_actions(self) -> Action:
        return Action(False, 0, False, 0, True)

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

    def get_actions(self) -> Action:
        return Action(False, 0, False, 0, True)

    def get_event_info(self):
        return f"\tname : {self.name} \n\tdesc : {self.effect} \n\tвы потеряли : {self.expense}"
    


class StockEvent(Event):
    def __init__(self, name, effect, symbol, price, flavor):
        super().__init__(name, effect)
        self.symbol = symbol
        self.price = price
        self.flavor = flavor

    def get_actions(self) -> Action:        
        return Action(True, 1, False, 0, True)

    def get_event_info(self):
        return f"\tname : {self.name} \n\tdesc : {self.flavor} \n\tФин инструмент : {self.symbol} по цене {self.price}"
    

class PropertyEvent(Event):
    def __init__(self, name, title, flavor_text, cost, mortgage, down_payment, cash_flow, bed, bath):
        super().__init__(name, title)
        self.title = title
        self.flavor_text = flavor_text
        self.cost = cost
        self.mortgage = mortgage
        self.down_payment = down_payment
        self.cash_flow = cash_flow
        self.bed = bed
        self.bath = bath

    def get_actions(self) -> Action:
        return Action(True, 200, True, 200, True)

    def get_event_info(self):
        return f"Название : {self.title} \n\tОписание : {self.flavor_text} \n\tСтоимость : {self.cost} \n\tИпотека : {self.mortgage} \n\tПервоначальный взнос : {self.down_payment} \n\tДенежный поток : {self.cash_flow} \n\tКоличество спален : {self.bed} \n\tКоличество ванных комнат : {self.bath}"


class BusinessEvent(Event):
    def __init__(self, name, effect, title, flavor_text, cost, mortgage, down_payment, cash_flow):
        super().__init__(name, effect)
        self.title = title
        self.flavor_text = flavor_text
        self.cost = cost
        self.mortgage = mortgage
        self.down_payment = down_payment
        self.cash_flow = cash_flow

    def get_actions(self) -> Action:
        return Action(True, 1, False, 0, True)

    def get_event_info(self):
        return f"Название : {self.title} \n\tОписание : {self.flavor_text} \n\tСтоимость : {self.cost} \n\tИпотека : {self.mortgage} \n\tПервоначальный взнос : {self.down_payment} \n\tДенежный поток : {self.cash_flow}"
