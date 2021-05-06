from abc import ABC, abstractmethod
from typing import Dict, Union
from enum import Enum

from order_book.book.book_iterators import PriceBinarySearch, OrderIdLinearSearch

class Book(ABC):
    @abstractmethod
    def find_by():
        pass
    @abstractmethod
    def insert():
        pass


class OrderBook(Book):
    def __init__(self):
        self.tickers: Dict[str, TickerOrderBook] = {}
        self.ids = {}
        self.ticker_id_map = {}

    def insert(self, order):
        if order.ticker not in self.tickers:
            tob = TickerOrderBook()
            tob.insert(order)
            self.tickers[order.ticker] = tob
            # If ticker isn't in self.tickers then it also isn't in 
            # self.ticker_id_map
            self.ticker_id_map[order.ticker] = set().add(order)
        else:
            self.tickers[order.ticker].insert(order)
        # Potentially unsafe operation to give us O(1) updates and "cancilations"
        self.ids[order.order_id] = order

    def update_order(self, order):
        # Since the index in self.ids points to same object as is
        # put in our OrderTree, we can reference that to get constant time
        # order updates. THIS OPERATION COULD BE UNSAFE!
        self.ids[order.order_id].size = order.size

    def cancel_order(self, order):
        # First find which ticker the order ID is associated with
        ticker = self._find_ticker_from_order_id(order)
        # Now do a linear search over the TickerOrderBook
        pass

    def _find_ticker_from_order_id(self, order):
        for ticker in self.ticker_id_map:
            ticker_set = self.ticker_id_map[ticker]
            # Python sets are hash sets, so this operation should O(1)
            if order.order_id in ticker_set:
                return ticker

    def __getitem__(self, ticker):
        return self.tickers[ticker]

    def find_by(self, ticker, attribute, **kwargs):
        return self.tickers[ticker].find_by(attribute, **kwargs)


class TickerOrderBook(Book):
    def __init__(self):
        self.orders = {"B": OrderTree(), "S": OrderTree()}

    def __getitem__(self, side):
        return self.orders[side]

    def insert(self, order):
        self.orders[order.side].insert(order)
    
    def find_by(self, attribute, **kwargs):
        search = self._search_factory(attribute)
        return search(self.orders).iterate(**kwargs)
        
    def _search_factory(self, attribute) -> Union[PriceBinarySearch, OrderIdLinearSearch]:
        supported_search = {SearchParams.PRICE: PriceBinarySearch,
                            SearchParams.ORDER: OrderIdLinearSearch}
        return supported_search[attribute]


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
                self._insert(order, node.left)
        else:
            if node.right is None:
                node.right = OrderNode(order)
            else:
                self._insert(order, node.right)

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


class SearchParams(Enum):
    PRICE = 1
    ORDER = 2