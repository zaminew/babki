from abc import ABC, abstractmethod

class Item(ABC):
    def __init__(self, name : str, quantity : int):
        self.name = name
        self.quantity = quantity

    @abstractmethod
    def get_item_info(self) -> str:
        pass
    
    @abstractmethod
    def copy(self, name=None, quantity=None):
        pass

class StockItem(Item):
    def __init__(self, name : str, price : int, quantity : int):
        super().__init__(name, quantity)
        self.name = name
        self.price = price

    def get_item_info(self) -> str:
        return f"\tname : {self.name}"
    
    def copy(self, name : str = None, price : int = None, quantity : int = None):
        new_item = StockItem(self.name, self.price, self.quantity)
        new_item.name = name if name is not None else self.name
        new_item.price = price if price is not None else self.price
        new_item.quantity = quantity if quantity is not None else self.quantity
        return new_item

class PropertyItem(Item):
    def __init__(self, name : str, price : int, mortgage : int, down_payment : int, cash_flow : int, bed : int, bath : int):
        super().__init__(name, quantity = 1)
        self.price = price
        self.mortgage = mortgage
        self.down_payment = down_payment
        self.cash_flow = cash_flow
        self.bed = bed
        self.bath = bath

    def get_item_info(self) -> str:
        return f"Название : {self.name} \n\tСтоимость : {self.price} \n\tИпотека : {self.mortgage} \n\tПервоначальный взнос : {self.down_payment} \n\tДенежный поток : {self.cash_flow} \n\tКоличество спален : {self.bed} \n\tКоличество ванных комнат : {self.bath}"

    def copy(self, name : str = None, price : int = None, mortgage : int = None, down_payment : int = None, cash_flow : int = None, bed : int = None, bath : int = None, quantity : int = None):
        new_item = PropertyItem(self.name, self.price, self.mortgage, self.down_payment, self.cash_flow, self.bed, self.bath)
        new_item.name = name if name is not None else self.name
        new_item.price = price if price is not None else self.price
        new_item.mortgage = mortgage if mortgage is not None else self.mortgage
        new_item.down_payment = down_payment if down_payment is not None else self.down_payment
        new_item.cash_flow = cash_flow if cash_flow is not None else self.cash_flow
        new_item.bed = bed if bed is not None else self.bed
        new_item.bath = bath if bath is not None else self.bath
        new_item.quantity = quantity if quantity is not None else self.quantity
        return new_item
    
class BusinessItem(Item):
    def __init__(self, name : str, price : int, mortgage : int, down_payment : int, cash_flow : int):
        super().__init__(name, quantity = 1)
        self.price = price
        self.mortgage = mortgage
        self.down_payment = down_payment
        self.cash_flow = cash_flow

    def get_item_info(self) -> str:
        return f"Название : {self.name} \n\tСтоимость : {self.price} \n\tИпотека : {self.mortgage} \n\tПервоначальный взнос : {self.down_payment} \n\tДенежный поток : {self.cash_flow}"
    
    def copy(self, name : str = None, price : int = None, mortgage : int = None, down_payment : int = None, cash_flow : int = None, quantity : int = None):
        new_item = BusinessItem(self.name, self.price, self.mortgage, self.down_payment, self.cash_flow)
        new_item.name = name if name is not None else self.name
        new_item.price = price if price is not None else self.price
        new_item.mortgage = mortgage if mortgage is not None else self.mortgage
        new_item.down_payment = down_payment if down_payment is not None else self.down_payment
        new_item.cash_flow = cash_flow if cash_flow is not None else self.cash_flow
        new_item.quantity = quantity if quantity is not None else self.quantity
        return new_item

# TODO add items
class СharityItem(Item): # TODO переделать под благотворительность
    def __init__(self, name : str):
        super().__init__(name, quantity = 1)
        
    def get_item_info(self) -> str:
        return f"Название : {self.name}"

class InsuranceItem(Item): # TODO переделать под страховку
    def __init__(self, name : str):
        super().__init__(name, quantity = 1)

    def get_item_info(self) -> str:
        return f"Название : {self.name}"
