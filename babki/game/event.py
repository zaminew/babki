from action import Action
from player import Player

class Event:
    def __init__(self, name, desc):
        self.name = name
        self.desc = desc
        self.input_requires = False

    def get_actions(self, player : Player) -> Action:
        return Action(False, 0, False, 0, True)
    
    def execute_action(self, action : Action, player : Player):
        pass

    def get_event_info(self):
        return f"\tname : {self.name} \n\tdesc : {self.desc}"
        #TODO наследники в результате должны вывести доступные действие с данным событием 
            # а пользователь может применить это действие на событии и получить результат
            # возможно понадобится несколько функций, вывод, ввод, результат. И это для одного шага


class ExpenseEvent(Event):
    def __init__(self, name, desc, cost, costMin, costMax, costStep, child):
        super().__init__(name, desc)
        self.cost = cost
        self.costMin = costMin
        self.costMax = costMax
        self.costStep = costStep
        self.child = child

    def get_actions(self, player : Player) -> Action:
        return Action(False, 0, False, 0, True)
    
    def execute_action(self, action : Action, player : Player):
        print('executed expense')
        if player.balance >= self.cost:
            player.balance -= self.cost
            return True
        else:
            return False
        
    def get_event_info(self):
        return f"\tname : {self.name} \n\tвы потеряли : {self.cost}"
    


class StockEvent(Event):
    def __init__(self, symbol, flavor, price, quantity = 0):
        super().__init__(symbol, flavor)
        self.symbol = symbol
        self.price = price
        self.flavor = flavor
        self.quantity = quantity

    def get_actions(self, player : Player) -> Action:      
        act = Action(False, 0, False, 0, True)
        amount_for_buy = player.balance // self.price

        if amount_for_buy > 0:
            act.buy = True
            act.buy_amount = amount_for_buy

        event_index = next((index for index, event in enumerate(player.stocks) if event.name == self.name), None)
        if event_index is not None:
            act.sell = True
            act.sell_amount = player.stocks[event_index].quantity
            
        return act
    
    def execute_action(self, action : Action, player : Player):
        if action.buy and self.get_actions(player).buy:
            if player.balance >= self.price * action.buy_amount:
                player.balance -= self.price * action.buy_amount
                event_index = next((index for index, event in enumerate(player.stocks) if event.name == self.name), None)
                if event_index is not None:
                    player.stocks[event_index].quantity += action.buy_amount
                else:
                    player.stocks.append(StockEvent(self.name, '', self.price, action.buy_amount))
            return True
        
        if action.sell and self.get_actions(player).sell:
            event_index = next((index for index, event in enumerate(player.stocks) if event.name == self.name), None)
            if event_index is not None and player.stocks[event_index].quantity >= action.sell_amount:
                player.stocks[event_index].quantity -= action.sell_amount
                player.balance += self.price * action.sell_amount
                if player.stocks[event_index].quantity <= 0:
                    del player.stocks[event_index]
            return True
        
        if action.check and self.get_actions(player).check:
            print('executed stock')
            return True
        
        print("error operation stock")
        return False

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

    def get_actions(self, player : Player) -> Action:
        return Action(True, 200, True, 200, True)
    
    def execute_action(self, action : Action, player : Player):
        print('executed property')
        return True

    def get_event_info(self):
        return f"Название : {self.title} \n\tОписание : {self.flavor_text} \n\tСтоимость : {self.cost} \n\tИпотека : {self.mortgage} \n\tПервоначальный взнос : {self.down_payment} \n\tДенежный поток : {self.cash_flow} \n\tКоличество спален : {self.bed} \n\tКоличество ванных комнат : {self.bath}"


class BusinessEvent(Event):
    def __init__(self, name, desc, title, flavor_text, cost, mortgage, down_payment, cash_flow):
        super().__init__(name, desc)
        self.title = title
        self.flavor_text = flavor_text
        self.cost = cost
        self.mortgage = mortgage
        self.down_payment = down_payment
        self.cash_flow = cash_flow

    def get_actions(self, player : Player) -> Action:
        return Action(True, 1, False, 0, True)
    
    def execute_action(self, action : Action, player : Player):
        print('executed bussness')
        return True

    def get_event_info(self):
        return f"Название : {self.title} \n\tОписание : {self.flavor_text} \n\tСтоимость : {self.cost} \n\tИпотека : {self.mortgage} \n\tПервоначальный взнос : {self.down_payment} \n\tДенежный поток : {self.cash_flow}"
