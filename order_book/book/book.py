from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict

class Book(ABC):
    @abstractmethod
    def find_by():
        pass


class OrderBookIterator(ABC):
    @abstractmethod
    def iterate():
        pass


class OrderBook(Book):
    def __init__(self):
        self.tickers: Dict[str, TickerOrderBook] = {}

    def add_new_order(self, order):
        if order.ticker not in self.tickers:
            tob = TickerOrderBook()
            tob.add(order)
            self.tickers[order.ticker] = tob
        else:
            self.tickers[order.ticker].add(order)

    def cancel_order(self, order):
        pass

    def update_order(self, order):
        pass

    def __getitem__(self, ticker):
        return self.tickers[ticker]

    def find_by(self, ticker, by_clause):
        '''
        Take param and search ticker by that clause
        '''
        return self.tickers[ticker].find_by(by_clause)


class TickerOrderBook(Book):
    def __init__(self):
        self.orders = {"B": OrderTree(), "S": OrderTree()}

    def add(self, order):
        # do binary search here find the correct place to slot in the new order.
        # This should be better than re-sorting on every add ie. O(ln(N)) VS O(Nln(N))
        self.orders[order.side].insert(order)
    
    def find_by(self, by_clause):
        pass


class OrderTree:
    def __init__(self):
        self.root = None

    def insert(self, order):
        if not self.root:
            self.root = OrderNode(order)
        else:
            self._insert(order, self.root)


    def _insert(self, order, node):
        if order.price <= node:
            if node.left is None:
                node.left = OrderNode(order)
            else:
                node.left = self._insert(order, node.left)
        else:
            if node.right is None:
                node.right = OrderNode(order)
            else:
                node.right = self._insert(order, node.right)


    def delete(self):
        pass

    def update(self):
        pass


class OrderNode:
    def __init__(self, order):
        self.order = order
        self.price = order.price
        self.left = None
        self.right = None

    def __eq__(self, compare) -> bool:
        return compare == self.price

    def __ne__(self, compare) -> bool:
        return compare != self.price

    def __le__(self, compare) -> bool:
        return self.price <= compare

    def __ge__(self, compare) -> bool:
        return self.price >= compare

    def __str__(self):
        return f"{self.order.order_id}|{self.price}"


class TickerOrderBookIterator(OrderBookIterator):
    pass
