import json
import random
import os

# Получаем путь к текущему файлу
current_dir = os.path.dirname(os.path.abspath(__file__))

# Формируем путь к файлу 'doodads.json'
eventsfilePath = os.path.join(current_dir, 'events.json')

class JsonLoader:
    @staticmethod
    def load(file_name):
        with open(file_name, 'r') as file:
            return json.load(file)

class Event:
    def __init__(self, name, effect):
        self.name = name
        self.effect = effect
        self.inputRequires = False

    def apply_effect(self, player):
        pass
        #TODO наследники в результате должны вывести доступные действие с данным событием 
            # а пользователь может применить это действие на событии и получить результат
            # возможно понадобится несколько функций, вывод, ввод, результат. И это для одного шага


class ExpenseEvent(Event):
    def __init__(self, name, effect, expenses_data):
        super().__init__(name, effect)
        self.expenses_data = expenses_data

    def apply_effect(self, player):
        expense = random.choice(self.expenses_data["doodads"])
        player.balance -= expense["cost"]
        print(f"{self.name}: {expense['title']} -{expense['cost']}")


class StockEvent(Event):
    def __init__(self, name, effect, stocks_data):
        super().__init__(name, effect)
        self.stocks_data = stocks_data

    def apply_effect(self, player):
        stock = random.choice(self.stocks_data["stocks"])
        self.inputRequires = True
        print(f"{self.name}: {stock['symbol']} цена за акцию сегодня ${stock['price']}")
        
        action = input("Хотите купить (buy) или продать (sell) акцию? ")

        if action.lower() == "buy":
            player.balance -= stock["price"]
            print(f"Вы купили акцию {stock['symbol']} за ${stock['price']}")
        elif action.lower() == "sell":
            player.balance += stock["price"]
            print(f"Вы продали акцию {stock['symbol']} за ${stock['price']}")
        else:
            print("Неверное действие. Попробуйте снова.")

        print(f"Баланс: ${player.balance}")


class Player:
    def __init__(self, name, balance, salary_level):
        self.name = name
        self.balance = balance
        self.salary_level = salary_level
        self.credits = 0

    def take_credit(self, amount):
        pass

    def repay_credit(self, amount):
        pass

    def calculate_balance(self):
        pass

class Game:
    def __init__(self, player, events_data, expenses_data):
        self.player = player
        self.events_data = events_data
        self.expenses_data = expenses_data
        self.current_step = 0
        self.months_passed = 0

    def generate_event(self):
        pass

    def play_step(self):
        pass

    def play_month(self):
        event = random.choice(self.events_data)
        event.apply_effect(self.player)
        if event.inputRequires:
            print("")
        self.current_step += 1
        
        print(f"Step: {self.current_step}")
        if self.current_step % 4 == 0:
            print("PAYDAY")
            player.balance += player.salary_level
        print(f"Balance: {self.player.balance}")
        

# Загрузка данных из JSON
events_data = [
    Event("Бизнес, недвижимость", "Купи продай большой и малый бизнес или недвижимость, а еще есть сетевые"),
    ExpenseEvent("Непредвиденные расходы", "Произошел неожиданный расход", JsonLoader.load(eventsfilePath)),
    StockEvent("Фондовый рынок", "Кпи продай акции облигации и другие инструменты", JsonLoader.load(eventsfilePath))
]

#TODO в самом событии будет указано что можно делать с этим событием и какие кнопки будут доступны а так же доступное колличество


player = Player("Player1", 10000, 1000)

game = Game(player, events_data, JsonLoader.load(eventsfilePath))

while True:
    game.play_month()
    input("Press Enter to continue...\n")


#TODO если будут события разного типа на одном шаге то можно попробовтаь написать функцию 
    # которая будет проверять как давно события этого типа генерировались и если давно то повышать вероятность

