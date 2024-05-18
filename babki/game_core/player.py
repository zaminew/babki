from typing import List
from item import *
from loan import Loan

class Player:
    def __init__(self, uniq_id, name, balance, salary_level):
        self.uniq_id = uniq_id
        self.name = name
        self.balance = balance
        self.salary_level = salary_level
        self.child : bool = False
        self.is_ready : bool = False
        self.action_taken : bool = False
        self.properties : List[PropertyItem] = []
        self.stocks : List[StockItem] = []
        self.businesses : List[BusinessItem] = []
        self.loan : Loan = Loan(self)
        
    def get_stock_index_by_name(self, name):
        return next((index for index, player_stock in enumerate(self.stocks) if player_stock.name == name), None)
   
    def get_cash_flow(self):
        flow = self.salary_level
        flow += sum(item.cash_flow for item in self.properties)
        flow += sum(item.cash_flow for item in self.businesses)
        flow -= self.loan.get_payment()
        #new_balance += sum(item.cash_flow for item in self.stocks)
        return flow

    def take_turn(self):
        self.action_taken = True

    def reset_turn(self):
        self.action_taken = False
        
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

