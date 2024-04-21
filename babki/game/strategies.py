from player import Player
from event import *
from action import Action

class ActionStrategy:
    def execute(self, player : Player, event : Event, amount : int):
        return False, 'function not implemented'

class BuyStrategy(ActionStrategy):
    def execute(self, player : Player, event : Event, amount : int):
        if amount <= 0: 
                return False, 'Ошибка! Количество для продажи должно быть больше 0'
        if isinstance(event, StockEvent):
            if player.balance >= event.price * amount:
                player.balance -= event.price * amount
                event_index = next((index for index, player_stock in enumerate(player.stocks) if player_stock.name == event.name), None)
                if event_index is not None:
                    player.stocks[event_index].quantity += amount
                else:
                    player.stocks.append(StockEvent(event.name, '', event.price, amount))
                return True, f'Вы купили {event.name} в количестве {amount} по цене {event.price} на сумму {event.price*amount}'
            else:
                return False, f'Вам не хватает {event.price * amount - player.balance} для покупки {amount}x {event.name} по {event.price}, за {event.price * amount}'
        elif isinstance(event, PropertyEvent):
            return False, 'buy Property function not implemented'
        elif isinstance(event, ExpenseEvent):
            return False, 'Вы не можете использовать покупку для этого события'
        else:
            return False, 'function not implemented'
class SellStrategy(ActionStrategy):
    def execute(self, player : Player, event : Event, amount : int):
        if amount <= 0: 
                return False, 'Ошибка! Количество для продажи должно быть больше 0'
        if isinstance(event, StockEvent):
            event_index = next((index for index, player_stock in enumerate(player.stocks) if player_stock.name == event.name), None)
            if event_index is not None:
                player_stock = player.stocks[event_index]
                if player_stock.quantity < amount:
                    return False, f'Вы не можете продать {event.name} в количестве {amount}, у вас есть только {player_stock.quantity}'
                player_stock.quantity -= amount
                player.balance += event.price * amount
                if player_stock.quantity <= 0:
                    del player.stocks[event_index]
                return True, f'Вы продали {event.name} в количестве {amount} по цене {event.price} на сумму {event.price*amount}'
            else:
                return False, f'У вас нет {event.name}'
        elif isinstance(event, PropertyEvent):
            return False, 'sell Property function not implemented'
        elif isinstance(event, ExpenseEvent):
            return False, 'Вы не можете использовать продажу для этого события'
        else:
            return False, 'function not implemented'
    
class CheckStrategy(ActionStrategy):
    def execute(self, player : Player, event : Event, amount : int):
        if isinstance(event, StockEvent):
            return True, 'Вы пропустили это событие'
        elif isinstance(event, PropertyEvent):
            return True, 'Вы пропустили это событие'
        elif isinstance(event, ExpenseEvent):
            if player.balance >= event.cost:
                player.balance -= event.cost
                return True, f'Вы потратили {event.cost} на {event.name}'
            else:
                return False, f'Вам не хватает {event.cost - player.balance} для покупки {event.name} за {event.cost}'
        else:
            return True, 'function not implemented'
        
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

if __name__ == '__main__':
    # Пример использования
    player = Player('Eugene', 10000, 1000)

    # Получение стратегии и ее выполнение
    buy_strategy = StrategyFactory.get_strategy(Action.BUY)
    sell_strategy = StrategyFactory.get_strategy(Action.SELL)
    check_strategy = StrategyFactory.get_strategy(Action.CHECK)

    if buy_strategy and check_strategy:
        print(buy_strategy.execute(player, StockEvent('MySymbol', 'description', 50, 2000), 1000)[1])
        print(buy_strategy.execute(player, StockEvent('MySymbol', 'description', 500, 2000), 10)[1])
        print(sell_strategy.execute(player, StockEvent('MySymbol', 'description', 500, 2000), 2)[1])
        print(sell_strategy.execute(player, StockEvent('MySymbol', 'description', 500, 2000), 8)[1])
        print(check_strategy.execute(player, ExpenseEvent('Наушники для компа', 'старые уже облезли', 5000, 100, 10000, 100, 0), 1)[1])
    else:
        print('unknown strategy')
    print(player.balance)
    print(player.get_assets_info())