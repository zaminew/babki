
class Event:
    def __init__(self, name, desc):
        self.name = name
        self.desc = desc
        self.input_requires = False
        self.quantity = 0

    def get_event_info(self):
        return f"\tname : {self.name} \n\tdesc : {self.desc}"

class ExpenseEvent(Event):
    def __init__(self, name, desc, cost, costMin, costMax, costStep, child):
        super().__init__(name, desc)
        self.cost = cost
        self.costMin = costMin
        self.costMax = costMax
        self.costStep = costStep
        self.child = child
        
    def get_event_info(self):
        return f"\tname : {self.name} \n\tвы потеряли : {self.cost}"
    


class StockEvent(Event):
    def __init__(self, symbol, desc, price, quantity):
        super().__init__(symbol, desc)
        self.symbol = symbol
        self.price = price
        self.flavor = desc
        self.quantity = quantity

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

    def get_event_info(self):
        return f"Название : {self.title} \n\tОписание : {self.flavor_text} \n\tСтоимость : {self.cost} \n\tИпотека : {self.mortgage} \n\tПервоначальный взнос : {self.down_payment} \n\tДенежный поток : {self.cash_flow}"
