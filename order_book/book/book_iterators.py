from abc import ABC, abstractmethod

class OrderBookIterator(ABC):
    @abstractmethod
    def iterate():
        pass


class PriceBinarySearch(OrderBookIterator):
    def __init__(self, orders):
        self.orders = orders

    def _find_max(self, bid_orders):
        if bid_orders is None:
            return -float("inf")
        left_max = self._find_max(bid_orders.left)
        right_max = self._find_max(bid_orders.right)
        if left_max >= bid_orders:
            return left_max
        elif right_max >= bid_orders:
            return right_max
        return bid_orders

    def _find_min(self, ask_orders):
        if ask_orders is None:
            return float("inf")
        left_min = self._find_min(ask_orders.left)
        right_min = self._find_min(ask_orders.right)
        if left_min <= ask_orders:
            return left_min
        elif right_min <= ask_orders:
            return right_min
        return ask_orders

    def iterate(self, **kwargs):
        max_bid = self._find_max(self.orders["B"].root)
        min_ask = self._find_min(self.orders["S"].root)
        return max_bid, min_ask


class OrderIdLinearSearch(OrderBookIterator):
    def __init__(self, orders):
        self.orders = orders

    def iterate(self, **kwargs):
        pass