class Action:
    def __init__(self, buy=0, sell=0, skip=0):
        self.buy = buy
        self.sell = sell
        self.skip = skip
        
    def __str__(self):
        return f"Buy: {self.buy}, Sell: {self.sell}, Skip: {self.skip}"


if __name__ == '__main__':
    actions = Action(buy=1, sell=0, skip=1)

    if actions.buy:
        print(f"Можно купить: {actions.buy}")
    if actions.sell:
        print(f"Можно продать: {actions.sell}")
    if actions.skip:
        print("Можно пропустить")