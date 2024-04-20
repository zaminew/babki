from player import Player
from event import *
from action import ActionNew

class ActionStrategy:
    def execute(self, player, event):
        return True, 'function not implemented'

class BuyStrategy(ActionStrategy):
    def execute(self, player, event):
        if isinstance(event, StockEvent):
            # Логика для покупки акций
            return True, 'buy stock function not implemented'
        elif isinstance(event, PropertyEvent):
            # Логика для покупки дома
            return True, 'buy property function not implemented'

class SellStrategy(ActionStrategy):
    def execute(self, player, event):
        if isinstance(event, StockEvent):
            # Логика для продажи акций
            return True, 'sell stock function not implemented'
        elif isinstance(event, PropertyEvent):
            # Логика для продажи дома
            return True, 'sell property function not implemented'

class CheckStrategy(ActionStrategy):
    def execute(self, player, event):
        if isinstance(event, StockEvent):
            # Логика для продажи акций
            return True, 'check stock function not implemented'
        elif isinstance(event, PropertyEvent):
            # Логика для продажи дома
            return True, 'check property function not implemented'

# Фабрика стратегий
class StrategyFactory:
    @staticmethod
    def get_strategy(action_type : ActionNew):
        if action_type == ActionNew.BUY:
            return BuyStrategy()
        elif action_type == ActionNew.SELL:
            return SellStrategy()
        elif action_type == ActionNew.CHECK:
            return CheckStrategy()
        else:
            return None

# Пример использования
player = Player('Eugene', 10000, 1000)

# Получение действия и события
action_type = "buy"  # Предположим, что это действие
event_type = "stock"  # Предположим, что это тип события

# Получение стратегии и ее выполнение
strategy = StrategyFactory.get_strategy(ActionNew.BUY)
if strategy:
    res = strategy.execute(player, StockEvent('MySymbol', 'description', 777))
    print(res)
else:
    print('unknown strategy')