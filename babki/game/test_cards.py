import unittest

from player import Player
from card import *
from action import Action

class TestCard(unittest.TestCase):
    def test_available_actions(self):
        player = Player("Eugene", 10000, 1000)
        
        stock_card = StockCard('stock', 'good stock', StockItem('STK1', 100, 500))
        self.assertIn(Action.BUY, stock_card.get_available_action(player))
        self.assertNotIn(Action.SELL, stock_card.get_available_action(player))
        self.assertIn(Action.SKIP, stock_card.get_available_action(player))

        stock_card = StockCard('stock', 'good stock', StockItem('STK1', 10000, 500))
        self.assertIn(Action.BUY, stock_card.get_available_action(player))
        self.assertNotIn(Action.SELL, stock_card.get_available_action(player))
        self.assertIn(Action.SKIP, stock_card.get_available_action(player))
        
        stock_card = StockCard('stock', 'good stock', StockItem('STK1', 100000, 500))
        self.assertNotIn(Action.BUY, stock_card.get_available_action(player))
        self.assertNotIn(Action.SELL, stock_card.get_available_action(player))
        self.assertIn(Action.SKIP, stock_card.get_available_action(player))
        
        stock_card = StockCard('stock', 'good stock', StockItem('STK1', 0, 500))
        self.assertIn(Action.BUY, stock_card.get_available_action(player))
        self.assertNotIn(Action.SELL, stock_card.get_available_action(player))
        self.assertIn(Action.SKIP, stock_card.get_available_action(player))
        
        stock_card = StockCard('stock', 'good stock', StockItem('STK1', 1, 500))
        stock_card.execute(player, Action.BUY, 1)
        self.assertIn(Action.BUY, stock_card.get_available_action(player))
        self.assertIn(Action.SELL, stock_card.get_available_action(player))
        self.assertIn(Action.SKIP, stock_card.get_available_action(player))
        
        stock_card = StockCard('stock', 'good stock', StockItem('STK1', 1, 500))
        stock_card.execute(player, Action.BUY, 500)
        self.assertIn(Action.BUY, stock_card.get_available_action(player))
        self.assertIn(Action.SELL, stock_card.get_available_action(player))
        self.assertIn(Action.SKIP, stock_card.get_available_action(player))
        
        stock_card = StockCard('stock', 'good stock', StockItem('STK1', 1, 500))
        stock_card.execute(player, Action.SELL, 500)
        self.assertIn(Action.BUY, stock_card.get_available_action(player))
        self.assertIn(Action.SELL, stock_card.get_available_action(player))
        self.assertIn(Action.SKIP, stock_card.get_available_action(player))

        player = Player("Eugene", 100, 1000)
        stock_card = StockCard('stock', 'good stock', StockItem('STK1', 1000, 500))
        stock_card.execute(player, Action.SELL, 1)
        self.assertNotIn(Action.BUY, stock_card.get_available_action(player))
        self.assertNotIn(Action.SELL, stock_card.get_available_action(player))
        self.assertIn(Action.SKIP, stock_card.get_available_action(player))


        player = Player("Eugene", 10000, 1000)
        property_card = PropertyCard('Жилье', 'good квартира', PropertyItem('Квартира', 100000, 90000, 1000, 100, 1, 1))
        self.assertIn(Action.BUY, property_card.get_available_action(player))
        self.assertNotIn(Action.SELL, property_card.get_available_action(player))
        self.assertIn(Action.SKIP, property_card.get_available_action(player))

        property_card = PropertyCard('Жилье', 'good квартира', PropertyItem('Квартира', 100000, 90000, 10000, 1000, 1, 1))
        self.assertIn(Action.BUY, property_card.get_available_action(player))
        self.assertNotIn(Action.SELL, property_card.get_available_action(player))
        self.assertIn(Action.SKIP, property_card.get_available_action(player))
        
        property_card = PropertyCard('Жилье', 'good квартира', PropertyItem('Квартира', 100000, 90000, 40000, 10000, 1, 1))
        self.assertNotIn(Action.BUY, property_card.get_available_action(player))
        self.assertNotIn(Action.SELL, property_card.get_available_action(player))
        self.assertIn(Action.SKIP, property_card.get_available_action(player))
        
        property_card = PropertyCard('Жилье', 'good квартира', PropertyItem('Квартира', 100000, 90000, 0, 0, 1, 1))
        self.assertIn(Action.BUY, property_card.get_available_action(player))
        self.assertNotIn(Action.SELL, property_card.get_available_action(player))
        self.assertIn(Action.SKIP, property_card.get_available_action(player))



        business_card = BusinessCard("my business", "stange business", BusinessItem("pizza", 10000, 9000, 1000, 100))
        self.assertIn(Action.BUY, business_card.get_available_action(player))
        self.assertNotIn(Action.SELL, business_card.get_available_action(player))
        self.assertIn(Action.SKIP, business_card.get_available_action(player))

        business_card = BusinessCard("my business", "stange business", BusinessItem("pizza", 10000, 9000, 10000, 100))
        self.assertIn(Action.BUY, business_card.get_available_action(player))
        self.assertNotIn(Action.SELL, business_card.get_available_action(player))
        self.assertIn(Action.SKIP, business_card.get_available_action(player))

        business_card = BusinessCard("my business", "stange business", BusinessItem("pizza", 10000, 9000, 100000, 100))
        self.assertNotIn(Action.BUY, business_card.get_available_action(player))
        self.assertNotIn(Action.SELL, business_card.get_available_action(player))
        self.assertIn(Action.SKIP, business_card.get_available_action(player))

        business_card = BusinessCard("my business", "stange business", BusinessItem("pizza", 10000, 9000, 0, 100))
        self.assertIn(Action.BUY, business_card.get_available_action(player))
        self.assertNotIn(Action.SELL, business_card.get_available_action(player))
        self.assertIn(Action.SKIP, business_card.get_available_action(player))

if __name__ == '__main__':
    unittest.main()
