from typing import List
from item import *

class Player:
    def __init__(self, name, balance, salary_level):
        self.name = name
        self.balance = balance
        self.salary_level = salary_level
        self.credit = 0
        self.child : bool = False
        self.is_ready : bool = False

        self.properties : List[PropertyItem] = []
        self.stocks : List[StockItem] = []
        self.businesses : List[BusinessItem] = []

    def take_credit(self, amount):
        pass

    def repay_credit(self, amount):
        pass

    def get_cash_flow(self):
        flow = self.salary_level
        flow += sum(item.cash_flow for item in self.properties)
        flow += sum(item.cash_flow for item in self.businesses)
        #new_balance += sum(item.cash_flow for item in self.stocks)
        return flow
        
    def get_assets_value(self):
        return sum(property.price for property in self.properties) + sum(stock.price for stock in self.stocks) + sum(business.price for business in self.businesses)

    def get_assets_info(self):
        return  {
            "property": [
                {
                    "name": property.name,
                    "price": property.price,
                    "mortgage": property.mortgage,
                    "down_payment": property.down_payment,
                    "cash_flow": property.cash_flow,
                    "bed": property.bed,
                    "bath": property.bath
                } for property in self.properties
            ],
            "stocks": [{"name": stock.name, "quantity": stock.quantity, "price": stock.price} for stock in self.stocks],
            "businesses": [
                {
                    "name": business.name,
                    "price": business.price,
                    "mortgage": business.mortgage,
                    "down_payment": business.down_payment,
                    "cash_flow": business.cash_flow
                } for business in self.businesses
            ]
        }
