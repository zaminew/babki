
class Item:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

    def get_item_info(self):
        return f"\tname : {self.name}"

class StockItem(Item):
    def __init__(self, name, price, quantity):
        super().__init__(name, quantity)
        self.name = name
        self.price = price

    def get_item_info(self):
        return f"\tname : {self.name}"

class PropertyItem(Item):
    def __init__(self, name, price, mortgage, down_payment, cash_flow, bed, bath):
        super().__init__(name, quantity = 1)
        self.price = price
        self.mortgage = mortgage
        self.down_payment = down_payment
        self.cash_flow = cash_flow
        self.bed = bed
        self.bath = bath

    def get_item_info(self):
        return f"Название : {self.name} \n\tСтоимость : {self.price} \n\tИпотека : {self.mortgage} \n\tПервоначальный взнос : {self.down_payment} \n\tДенежный поток : {self.cash_flow} \n\tКоличество спален : {self.bed} \n\tКоличество ванных комнат : {self.bath}"

class BusinessItem(Item):
    def __init__(self, name, price, mortgage, down_payment, cash_flow):
        super().__init__(name, quantity = 1)
        self.price = price
        self.mortgage = mortgage
        self.down_payment = down_payment
        self.cash_flow = cash_flow

    def get_item_info(self):
        return f"Название : {self.title} \n\tСтоимость : {self.price} \n\tИпотека : {self.mortgage} \n\tПервоначальный взнос : {self.down_payment} \n\tДенежный поток : {self.cash_flow}"


# TODO add items
class СharityItem(Item): # TODO переделать под благотворительность
    def __init__(self, name):
        super().__init__(name, quantity = 1)
        
    def get_item_info(self):
        return f"Название : {self.name}"

class InsuranceItem(Item): # TODO переделать под страховку
    def __init__(self, name):
        super().__init__(name, quantity = 1)

    def get_item_info(self):
        return f"Название : {self.name}"
