class Action:
    def __init__(self, buy=0, sell=0, skip=0):
        self.buy = buy
        self.sell = sell
        self.skip = skip
        
    def __str__(self):
        return f"Buy: {self.buy}, Sell: {self.sell}, Skip: {self.skip}"
    
    def is_active(self):
        return any([self.buy, self.sell, self.skip])
