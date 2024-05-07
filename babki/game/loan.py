from abc import ABC, abstractmethod
from typing import TypeVar
import math

class Loan:
    def __init__(self, player):
        self.player = player
        self.amount = 0
        self.rate = 4
    
    def take(self, amount):
        if amount <= 0:
            return False, f'Сумма кредита {amount} не может быть отрицательной, либо нулевой'
        
        if math.ceil(amount * self.rate / 100) <= self.player.get_cash_flow():
            self.amount += amount
            self.player.balance += amount
            return True, f'Вы взяли кредит на сумму {amount}, новый долг {self.amount}'
        else:
            return False, 'Запрошенная сумма превышает Ваш лимит, вам отказано в кредите'

    def repay(self, amount):
        if amount <= 0:
            return False, f'Сумма для погашения {amount} не может быть отрицательной, либо нулевой'
            
        if self.amount < amount:
            return False, f'Сумма для погашения {amount} не может превышать сумму долга {self.amount}'
        
        if self.player.balance < amount:
            return False, f'Вам не хватает средств {self.player.balance} для погашения долга {self.amount}'
        
        self.amount -= amount
        self.player.balance -= amount
        return True, f'Вы погасили долг на сумму {amount}, остаток {self.amount}'
    
    def get_payment(self):
        return math.ceil(self.amount * self.rate / 100)