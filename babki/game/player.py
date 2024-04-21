from typing import List
from event import *

class Player:
    def __init__(self, name, balance, salary_level):
        self.name = name
        self.balance = balance
        self.salary_level = salary_level
        self.credit = 0
        self.child : bool = False
        self.is_ready : bool = False

        self.properties : List[PropertyEvent] = []
        self.stocks : List[StockEvent] = []
        self.businesses : List[BusinessEvent] = []

    def take_credit(self, amount):
        pass

    def repay_credit(self, amount):
        pass

    def calculate_balance(self):
        pass

    def get_assets_value(self):
        return sum(property.cost for property in self.properties) + sum(stock.price for stock in self.stocks) + sum(business.cost for business in self.businesses)

    def get_assets_info(self):
        return  {
            "properties": [property.name for property in self.properties],
            "stocks": [{"name": stock.name, "quantity": stock.quantity} for stock in self.stocks],
            "businesses": [business.name for business in self.businesses]
        }
