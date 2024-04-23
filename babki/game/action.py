from enum import Enum

class EnumStr(Enum):
    def __str__(self):
        return self.value
    
class Action(EnumStr):
    BUY = 'buy'
    SELL = 'sell'
    CHECK = 'check'
    GET = 'get'