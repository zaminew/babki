from item import *
from player import Player
from action import Action

class Card:
    def __init__(self, title, description):
        self.title = title
        self.desc = description
        self.input_requires = False

    def get_available_actions(self):
        actions = ()
        if False:
            actions += (Action.BUY,)
        if False:
            actions += (Action.SELL,)
        if False:
            actions += (Action.SKIP,)
        return actions

    def get_card_info(self):
        return f"\ttitle : {self.title} \n\tdesc : {self.desc}"
    
    def buy(self, player : Player):
        pass

    def sell(self):
        pass

    def skip(self):
        pass

class ExpenseCard(Card):
    def __init__(self, title, description, price, child):
        super().__init__(title, description)
        self.price = price
        self.child = child

    def get_card_info(self):
        return f"\ttitle : {self.title} \n\tвы потеряли : {self.price}"
    
    def buy(self):
        pass

    def sell(self):
        pass

    def skip(self):
        pass
    
class StockCard(Card):
    def __init__(self, title, description, stock_item : StockItem):
        super().__init__(title, description)
        self.stock_item : StockItem = stock_item
        
    def get_card_info(self):
        return f"\ttitle : {self.title}"
    
    def buy(self):
        pass

    def sell(self):
        pass

    def skip(self):
        pass

class PropertyCard(Card):
    def __init__(self, title, description, property_item : PropertyItem):
        super().__init__(title, description)
        self.property_item : PropertyItem = property_item
        
    def get_card_info(self):
        return f"\ttitle : {self.title}"

    def buy(self):
        pass

    def sell(self):
        pass

    def skip(self):
        pass
    
class BusinessCard(Card):
    def __init__(self, title, description, business_item : BusinessItem):
        super().__init__(title, description)
        self.business_item : BusinessItem = business_item
        
    def get_card_info(self):
        return f"\ttitle : {self.title}"
    
    def buy(self):
        pass

    def sell(self):
        pass

    def skip(self):
        pass

class СharityCard(Card):
    def __init__(self, title, description, charity_item : СharityItem):
        super().__init__(title, description)
        self.charity_item : СharityItem = charity_item
        
    def get_card_info(self):
        return f"\ttitle : {self.title}"
    
    def buy(self):
        pass

    def sell(self):
        pass

    def skip(self):
        pass
    
class InsuranceCard(Card):
    def __init__(self, name, description, insurance_item : InsuranceItem):
        super().__init__(name, description)
        self.insurance_item : InsuranceItem = insurance_item
        
    def get_card_info(self):
        return f"\ttitle : {self.title}"
    
    def buy(self):
        pass

    def sell(self):
        pass

    def skip(self):
        pass



if __name__ == '__main__':
    card = Card('title', 'desc')
    av = card.get_available_actions()
    if Action.BUY in av:
        print("Action.BUY есть в кортеже")
    if Action.SELL in av:
        print("Action.SELL есть в кортеже")
    if Action.SKIP in av:
        print("Action.SKIP есть в кортеже")
    print(av)