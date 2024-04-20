from enum import Enum

class Action:
    def __init__(self, buy=False, buy_amount=0, sell=False, sell_amount=0, check=False):
        self.buy = buy
        self.buy_amount = buy_amount
        self.sell = sell
        self.sell_amount = sell_amount
        self.check = check

class EnumStr(Enum):
    def __str__(self):
        return self.value
    
class ActionNew(EnumStr):
    BUY = 'buy'
    SELL = 'sell'
    CHECK = 'check'