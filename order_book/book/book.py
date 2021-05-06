from abc import ABC, abstractmethod
from typing import Dict

class Book(ABC):
    @abstractmethod
    def find_by():
        pass
    @abstractmethod
    def insert():
        pass


class OrderBookIterator(ABC):
    @abstractmethod
    def iterate():
        pass


class OrderBook(Book):
    def __init__(self):
        self.tickers: Dict[str, TickerOrderBook] = {}
        self.ids = {}

    def insert(self, order):
        if order.ticker not in self.tickers:
            tob = TickerOrderBook()
            tob.insert(order)
            self.tickers[order.ticker] = tob
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
        # Use the same pointer trick to "cancel" the order
        # Canceled orders will still be held for a period of time
        # But can be removed at a later time
        self.ids[order.order_id].action = order.action

    def __getitem__(self, ticker):
        return self.tickers[ticker]

    def find_by(self, ticker):
        return self.tickers[ticker].find_by()


class TickerOrderBook(Book):
    def __init__(self):
        self.orders = {"B": OrderTree(), "S": OrderTree()}

    def __getitem__(self, side):
        return self.orders[side]

    def insert(self, order):
        # do binary search here find the correct place to slot in the new order.
        # This should be better than re-sorting on every add ie. O(ln(N)) VS O(Nln(N))
        self.orders[order.side].insert(order)
    
    def find_by(self):
        max_buy = self._find_max(self.orders["B"].root)
        min_ask = self._find_min(self.orders["S"].root)
        return max_buy, min_ask

    def _find_max(self, buy_orders):
        if buy_orders is None:
            return 0
        while buy_orders.right is not None:
            if buy_orders.right.order.price >= buy_orders.price:
                return self._find_max(buy_orders.right)
        return buy_orders


    def _find_min(self, ask_orders):
        if ask_orders is None:
            return 0
        while ask_orders.left is not None:
            if ask_orders.left.order.price <= ask_orders.price:
                return self._find_min(ask_orders.left)
        return ask_orders


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


class TickerOrderBookIterator(OrderBookIterator):
    pass
