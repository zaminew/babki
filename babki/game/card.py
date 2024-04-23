from item import *

class Card:
    def __init__(self, title, description):
        self.title = title
        self.desc = description
        self.input_requires = False

    def get_card_info(self):
        return f"\ttitle : {self.title} \n\tdesc : {self.desc}"

class ExpenseCard(Card):
    def __init__(self, title, description, price, child):
        super().__init__(title, description)
        self.price = price
        self.child = child
        
    def get_card_info(self):
        return f"\ttitle : {self.title} \n\tвы потеряли : {self.price}"
    
class StockCard(Card):
    def __init__(self, title, description, stock_item : StockItem):
        super().__init__(title, description)
        self.stock_item : StockItem = stock_item
        
    def get_card_info(self):
        return f"\ttitle : {self.title}"

class PropertyCard(Card):
    def __init__(self, title, description, property_item : PropertyItem):
        super().__init__(title, description)
        self.property_item : PropertyItem = property_item
        
    def get_card_info(self):
        return f"\ttitle : {self.title}"
    
class BusinessCard(Card):
    def __init__(self, title, description, business_item : BusinessItem):
        super().__init__(title, description)
        self.business_item : BusinessItem = business_item
        
    def get_card_info(self):
        return f"\ttitle : {self.title}"

class СharityCard(Card):
    def __init__(self, title, description, charity_item : СharityItem):
        super().__init__(title, description)
        self.charity_item : СharityItem = charity_item
        
    def get_card_info(self):
        return f"\ttitle : {self.title}"
    
class InsuranceCard(Card):
    def __init__(self, name, description, insurance_item : InsuranceItem):
        super().__init__(name, description)
        self.insurance_item : InsuranceItem = insurance_item
        
    def get_card_info(self):
        return f"\ttitle : {self.title}"