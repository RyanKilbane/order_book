from abc import ABC, abstractmethod
from order_book.order.order import Order
from order_book.book.exceptions import NoTickerException
from typing import Dict, Set, Union
from enum import Enum

from order_book.book.book_iterators import PriceBinarySearch, OrderIdSearch
from order_book.book.search_builder import SearchBuilder, SearchParams

class Book(ABC):
    @abstractmethod
    def find_by():
        pass
    @abstractmethod
    def insert():
        pass
    @abstractmethod
    def update_order():
        pass
    @abstractmethod
    def cancel_order():
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
            self.ticker_id_map[order.ticker] = set()
            self.ticker_id_map[order.ticker].add(order.order_id)
            self.ids[order.order_id] = order
        else:
            self.tickers[order.ticker].insert(order)
            # Potentially unsafe operation to give us O(1) updates
            self.ids[order.order_id] = order
            self.ticker_id_map[order.ticker].add(order.order_id)

    def update_order(self, order):
        # Since the index in self.ids points to same object as is
        # put in our OrderTree, we can reference that to get constant time
        # order updates. THIS OPERATION COULD BE UNSAFE!
        self.ids[order.order_id].size = order.size

    def cancel_order(self, order, *kwargs):
        # First find which ticker the order ID is associated with
        ticker = self._find_ticker_from_order_id(order)
        # Now do a linear search over the TickerOrderBook
        ticker: TickerOrderBook = self.tickers[ticker]
        ticker.cancel_order(order)

    def _find_ticker_from_order_id(self, order):
        for ticker in self.ticker_id_map:
            ticker_set: Set[Order] = self.ticker_id_map[ticker]
            # Python sets are hash sets, so this operation should be O(1)
            # which means finding a ticker from an order should only be bound
            # by the number of tickers. Hopefully tickers << orders.
            if order.order_id in ticker_set:
                return ticker

    def __getitem__(self, ticker):
        if ticker not in self.tickers:
            raise NoTickerException(f"The requested ticker: {ticker} doesn't exist")
        return self.tickers[ticker]

    def find_by(self, ticker, search_type, **kwargs):
        return self[ticker].find_by(search_type)


class TickerOrderBook(Book):
    def __init__(self):
        self.orders = {"B": OrderTree(), "S": OrderTree()}

    def __getitem__(self, side):
        return self.orders[side]

    def insert(self, order):
        self.orders[order.side].insert(order)

    def cancel_order(self, order, **kwargs):
        '''
        Cancel order is really a rebuild of the tree... not a great solution, but it's a solution
        Should hopefully give us O(N) cancelations, not as good as I would want, but I think it's 
        about as good as we can get. Maybe build a secondary tree, using deep copy, I'm not sure.
        '''
        new_orders = {"B": OrderTree(), "S": OrderTree()}
        search_params = SearchBuilder().add_search("order").add_traversal("inorder").build()
        bids, asks = self.find_by(search_params)
        for bid in bids:
            if bid.order.order_id == order.order_id:
                continue
            else:
                new_orders["B"].insert(bid.order)
        
        for ask in asks:
            if ask.order.order_id == order.order_id:
                continue
            else:
                new_orders["S"].insert(ask.order)
        # Now we've re built the OrderTree's without the canceled order
        # Overwrite the old OrderTree
        self.orders = new_orders

    def update_order():
        pass

    def find_by(self, search_type):
        search = self._search_factory(search_type)
        return search(self.orders).iterate(search_type)
        
    def _search_factory(self, search_type: SearchParams) -> Union[PriceBinarySearch, OrderIdSearch]:
        supported_search = {"price": PriceBinarySearch,
                            "order": OrderIdSearch}
        return supported_search[search_type.search_type]


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
        return f"{str(self.order)}"


# class SearchParams(Enum):
#     PRICE = 1
#     ORDER = 2