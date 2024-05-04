from item import *
from player import Player
from action import *

class Card:
    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.input_requires = False

    def get_available_action(self, player : Player) -> Action:
        action = Action()
        if False:
            action.buy = 0
        if False:
            action.sell = 0
        if False:
            action.skip = 0
        return action

    def get_card_info(self, player : Player):
        return f"\ttitle : {self.title} \n\tdesc : {self.description}"

    def execute(self, player : Player, action : Action):
        pass

class SalaryCard(Card):
    def __init__(self, title, description):
        super().__init__(title, description)

    def get_available_action(self, player : Player) -> Action:
        return Action(skip=1)
    
    def get_card_info(self, player : Player):
        card_info = f"title : {self.title}\ndescription : {self.description}"
        player_info = f'ваш баланс: {player.balance}'\
                        f'\n+денежный поток: {player.get_cash_flow()}'\
                        f'\n\nновый баланс: {player.balance+player.get_cash_flow()}'
        return card_info + player_info

    def execute(self, player : Player, action : Action):
        if action.skip:
            return self._skip(player)
        else:
            return False, f'это действие сейчас недоступно'

    def _skip(self, player : Player):
        cash_flow = player.get_cash_flow()
        player.balance += cash_flow
        return True, f'Вы получили {cash_flow}'

class ExpenseCard(Card):
    def __init__(self, title, description, price, child):
        super().__init__(title, description)
        self.price = price
        self.child = child

    def get_available_action(self, player : Player) -> Action:
        action = Action()
        if player.balance >= self.price:
            action.skip = 1
        return action
    
    def get_card_info(self, player : Player):
        card_info = f"title : {self.title}\ndescription : {self.description}"\
                    f"\n\nprice : {self.price}, child : {self.child}"
        return card_info

    def execute(self, player : Player, action : Action):
        if action.skip:
            return self._skip(player)
        else:
            return False, f'это действие сейчас недоступно'

    def _skip(self, player : Player):
        if player.balance >= self.price:
            player.balance -= self.price
            return True, f'Вы потратили {self.price} на {self.title}'
        else:
            return False, f'Вам не хватает {self.price - player.balance} для покупки {self.title} за {self.price}'

class StockCard(Card):
    def __init__(self, title, description, stock_item : StockItem):
        super().__init__(title, description)
        self.stock_item : StockItem = stock_item

    def get_available_action(self, player : Player) -> Action:
        action = Action()
        enough_for_buy = player.balance // self.stock_item.price
        available_for_buy = self.stock_item.quantity
        action.buy = min(enough_for_buy, available_for_buy)
        item_index = player.get_stock_index_by_name(self.stock_item.name)
        action.sell = player.stocks[item_index].quantity if item_index is not None else 0
        action.skip = 1
        return action
        
    def get_card_info(self, player : Player):
        card_info = f"title : {self.title}\ndescription : {self.description}"
        item_info = f"\n\nitem : "\
                            f"\n\tname : {self.stock_item.name}"\
                            f"\n\tprice : {self.stock_item.price}"\
                            f"\n\tquantity : {self.stock_item.quantity}"
        return card_info + item_info

    def execute(self, player : Player, action : Action):
        if action.buy:
            return self._buy(player, action.buy)
        elif action.sell:
            return self._sell(player, action.sell)
        elif action.skip:
            return True, f'Вы пропустили это событие'
        else:
            return False, f'это действие сейчас недоступно'

    def _buy(self, player : Player, amount : int):
        if amount > self.stock_item.quantity:
            return False, f'Вы не можете купить {self.stock_item.name} в количестве {amount}, в продаже доступно только {self.stock_item.quantity}'
        if player.balance >= self.stock_item.price * amount:
            player.balance -= self.stock_item.price * amount
            item_index = player.get_stock_index_by_name(self.stock_item.name)
            if item_index is not None:
                old_price = player.stocks[item_index].price
                old_quantity = player.stocks[item_index].quantity
                new_price = self.stock_item.price
                new_quantity = amount
                
                total_value = (old_price * old_quantity) + (new_price * new_quantity)
                total_quantity = old_quantity + new_quantity
                average_price = int(round(total_value / total_quantity, 0))
                
                player.stocks[item_index].quantity += amount
                player.stocks[item_index].price = average_price
            else:
                player.stocks.append(self.stock_item.copy(quantity=amount))
            return True, f'Вы купили {self.stock_item.name} в количестве {amount} по цене {self.stock_item.price} на сумму {self.stock_item.price*amount}'
        else:
            return False, f'Вам не хватает {self.stock_item.price * amount - player.balance} для покупки {amount}x {self.stock_item.name} по {self.stock_item.price}, за {self.stock_item.price * amount}'

    def _sell(self, player : Player, amount : int):
        item_index = next((index for index, player_stock in enumerate(player.stocks) if player_stock.name == self.stock_item.name), None)
        if item_index is not None:
            player_stock = player.stocks[item_index]
            if player_stock.quantity < amount:
                return False, f'Вы не можете продать {self.stock_item.name} в количестве {amount}, у вас есть только {player_stock.quantity}'
            player_stock.quantity -= amount
            player.balance += self.stock_item.price * amount
            if player_stock.quantity <= 0:
                del player.stocks[item_index]
            return True, f'Вы продали {self.stock_item.name} в количестве {amount} по цене {self.stock_item.price} на сумму {self.stock_item.price*amount}'
        else:
            return False, f'У вас нет {self.stock_item.name}'

class PropertyCard(Card):
    def __init__(self, title, description, property_item : PropertyItem):
        super().__init__(title, description)
        self.property_item : PropertyItem = property_item

    def get_available_action(self, player : Player) -> Action:
        action = Action()
        if player.balance >= self.property_item.down_payment:
            action.buy = 1
        action.skip = 1
        return action
    
    def get_card_info(self, player : Player):
        card_info = f"title : {self.title}\ndescription : {self.description}"
        item_info = f"\n\nitem : "\
                            f"\n\tname : {self.property_item.name}"\
                            f"\n\tprice : {self.property_item.price}"\
                            f"\n\tmortgage : {self.property_item.mortgage}"\
                            f"\n\tdown_payment : {self.property_item.down_payment}"\
                            f"\n\tcash_flow : {self.property_item.cash_flow}"\
                            f"\n\tbed : {self.property_item.bed}, bath : {self.property_item.bath}"
        return card_info + item_info

    def execute(self, player : Player, action : Action):
        if action.buy:
            return self._buy(player)
        elif action.sell:
            return self._sell(player)
        elif action.skip:
            return True, f'Вы пропустили это событие'

    def _buy(self, player : Player):
        if player.balance >= self.property_item.down_payment:
            player.balance -= self.property_item.down_payment
            player.properties.append(self.property_item.copy())
            return True, f'Вы купили {self.property_item.name} по цене {self.property_item.price}, ипотека {self.property_item.mortgage}, первоначальный взнос {self.property_item.down_payment}'
        else: 
            return False, f'Вам не хватает {self.property_item.down_payment - player.balance} на первоначальный взнос для покупки {self.property_item.name} по цене {self.property_item.price}, ипотека {self.property_item.mortgage}, первоначальный взнос {self.property_item.down_payment}'

    def _sell(self, player : Player):
        return False, f'это действие сейчас недоступно, продажа квартиры пока планируется отдельной картой'

class BusinessCard(Card):
    def __init__(self, title, description, business_item : BusinessItem):
        super().__init__(title, description)
        self.business_item : BusinessItem = business_item

    def get_available_action(self, player : Player) -> Action:
        action = Action()
        if player.balance >= self.business_item.down_payment:
            action.buy = 1
        action.skip = 1
        return action
        
    def get_card_info(self, player : Player):
        card_info = f"title : {self.title}\ndescription : {self.description}"
        item_info = f"\n\nitem : "\
                            f"\n\tname : {self.business_item.name}"\
                            f"\n\tprice : {self.business_item.price}"\
                            f"\n\tmortgage : {self.business_item.mortgage}"\
                            f"\n\tdown_payment : {self.business_item.down_payment}"\
                            f"\n\tcash_flow : {self.business_item.cash_flow}"
        return card_info + item_info

    def execute(self, player : Player, action : Action):
        if action.buy:
            return self._buy(player)
        elif action.sell:
            return self._sell(player)
        elif action.skip:
            return True, f'Вы пропустили это событие'
        else:
            return False, f'это действие сейчас недоступно'
        
    def _buy(self, player : Player):
        if player.balance >= self.business_item.down_payment:
            player.balance -= self.business_item.down_payment
            player.businesses.append(self.business_item.copy())
            return True, f'Вы купили {self.business_item.name} по цене {self.business_item.price}, ипотека {self.business_item.mortgage}, первоначальный взнос {self.business_item.down_payment}'
        else: 
            return False, f'Вам не хватает {self.business_item.down_payment - player.balance} на первоначальный взнос для покупки {self.business_item.name} по цене {self.business_item.price}, ипотека {self.business_item.mortgage}, первоначальный взнос {self.business_item.down_payment}'

    def _sell(self, player : Player):
        return False, f'это действие сейчас недоступно, продажа квартиры пока планируется отдельной картой'

# TODO add card
class СharityCard(Card):
    def __init__(self, title, description, charity_item : СharityItem):
        super().__init__(title, description)
        self.charity_item : СharityItem = charity_item

    def get_available_action(self, player : Player) -> Action:
        action = Action()
        if False:
            action.buy = 0
        if False:
            action.sell = 0
        if True:
            action.skip = 0
        return action
        
    def get_card_info(self, player : Player):
        return f"\ttitle : {self.title}"

    def execute(self, player : Player, action : Action):
        pass

    def _buy(self):
        pass

    def _sell(self):
        pass

    def _skip(self):
        pass

class InsuranceCard(Card):
    def __init__(self, name, description, insurance_item : InsuranceItem):
        super().__init__(name, description)
        self.insurance_item : InsuranceItem = insurance_item

    def get_available_action(self, player : Player):
        action = Action()
        if False:
            action.buy = 0
        if False:
            action.sell = 0
        if True:
            action.skip = 0
        return action
        
    def get_card_info(self, player : Player):
        return f"\ttitle : {self.title}"

    def execute(self, player : Player, action : Action, amount : int):
        pass

    def _buy(self):
        pass

    def _sell(self):
        pass

    def _skip(self):
        pass
