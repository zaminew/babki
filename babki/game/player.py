from typing import List
from item import *
import math

class Player:
    def __init__(self, name, balance, salary_level):
        self.name = name
        self.balance = balance
        self.salary_level = salary_level
        self.loan = 0
        self.loan_rate = 4
        self.child : bool = False
        self.is_ready : bool = False

        self.properties : List[PropertyItem] = []
        self.stocks : List[StockItem] = []
        self.businesses : List[BusinessItem] = []
        
    def get_stock_index_by_name(self, name):
        return next((index for index, player_stock in enumerate(self.stocks) if player_stock.name == name), None)

    def take_loan(self, amount):
        if amount <= 0:
            return False, 'Сумма кредита не может быть отрицательной, либо нулевой'
        
        if math.ceil(amount * self.loan_rate / 100) <= self.get_cash_flow():
            self.loan += amount
            self.balance += amount
            return True, f'Вы взяли кредит на сумму {amount}'
        else:
            return False, 'Запрошенная сумма превышает Ваш лимит, вам отказано в кредите'

    def repay_loan(self, amount):
        if amount <= 0:
            return False, 'Сумма для погашения не может быть отрицательной, либо нулевой'
            
        if self.loan < amount:
            return False, 'Сумма для погашения не может превышать сумму долга'
        
        if self.balance < amount:
            return False, 'Вам не хватает средств для погашения долга'
        
        self.loan -= amount
        self.balance -= amount
        return True, f'Вы погасили долг на сумму {amount}'
    
    def get_loan_payment(self):
        return math.ceil(self.loan * self.loan_rate / 100)
    
    def get_cash_flow(self):
        flow = self.salary_level
        flow += sum(item.cash_flow for item in self.properties)
        flow += sum(item.cash_flow for item in self.businesses)
        flow -= self.get_loan_payment()
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


if __name__ == '__main__':
    player = Player('Eugene', 3000, 100)
    print(f'balance: {player.balance}')
    player.businesses.append(BusinessItem('', 0, 0, 0, 1000))
    
    print(player.take_loan(25001))
    print(f'balance: {player.balance}, loan: {player.loan}, rate: {player.loan_rate}, pay: {player.get_loan_payment()}')
    print(player.get_cash_flow())
    
    print('\n')
    print(player.repay_loan(24001))
    print(f'balance: {player.balance}, loan: {player.loan}, rate: {player.loan_rate}, pay: {player.get_loan_payment()}')
    print(player.get_cash_flow())

    
    