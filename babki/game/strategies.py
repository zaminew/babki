from player import Player
from event import *
from action import Action

class ActionStrategy:
    def execute(self, player : Player, event : Event, amount : int):
        return False, 'function not implemented'

class BuyStrategy(ActionStrategy):
    def execute(self, player : Player, event : Event, amount : int):
        if isinstance(event, StockEvent):
            return True, f'Вы купили {event.name} в количестве {amount} по цене {event.price} на сумму {event.price*amount}'
        elif isinstance(event, PropertyEvent):
            return False, 'buy Property function not implemented'
        elif isinstance(event, ExpenseEvent):
            return False, 'Вы не можете использовать покупку для этого события'
        
class SellStrategy(ActionStrategy):
    def execute(self, player : Player, event : Event, amount : int):
        if isinstance(event, StockEvent):
            return True, f'Вы продали {event.name} в количестве {amount} по цене {event.price} на сумму {event.price*amount}'
        elif isinstance(event, PropertyEvent):
            return False, 'sell Property function not implemented'
        elif isinstance(event, ExpenseEvent):
            return False, 'Вы не можете использовать продажу для этого события'
        
class CheckStrategy(ActionStrategy):
    def execute(self, player : Player, event : Event, amount : int):
        if isinstance(event, StockEvent):
            return True, 'Вы пропустили это событие'
        elif isinstance(event, PropertyEvent):
            return True, 'Вы пропустили это событие'
        elif isinstance(event, ExpenseEvent):
            if player.balance >= event.cost:
                player.balance -= event.cost
                return True, f'Вы потеряли {event.cost} на безделушки'
            else:
                return False, f'Вам не хватает {event.cost - player.balance} для покупки {event.name} за {event.cost}'
        
# Фабрика стратегий
class StrategyFactory:
    @staticmethod
    def get_strategy(action_type : Action):
        if action_type == Action.BUY:
            return BuyStrategy()
        elif action_type == Action.SELL:
            return SellStrategy()
        elif action_type == Action.CHECK:
            return CheckStrategy()
        else:
            return None


# Пример использования
player = Player('Eugene', 10000, 1000)

# Получение стратегии и ее выполнение
buy_strategy = StrategyFactory.get_strategy(Action.BUY)
check_strategy = StrategyFactory.get_strategy(Action.CHECK)

if buy_strategy and check_strategy:
    buy_res = buy_strategy.execute(player, StockEvent('MySymbol', 'description', 777), 100)
    check_res = check_strategy.execute(player, ExpenseEvent('Наушники для компа', 'старые уже облезли', 50000, 100, 10000, 100, 0), 100)
    print(buy_res[1] + '\n' + check_res[1])
else:
    print('unknown strategy')
print(player.balance)