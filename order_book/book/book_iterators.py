from abc import ABC, abstractmethod

class OrderBookIterator(ABC):
    @abstractmethod
    def iterate():
        pass


class PriceBinarySearch(OrderBookIterator):
    def __init__(self, orders):
        self.orders = orders

    def _find_max(self, buy_orders):
        if buy_orders is None:
            return -float("inf")
        left_max = self._find_max(buy_orders.left)
        right_max = self._find_max(buy_orders.right)
        if left_max >= buy_orders:
            return left_max
        elif right_max >= buy_orders:
            return right_max
        return buy_orders


    def _find_min(self, ask_orders):
        if ask_orders is None:
            return float("inf")
        left_min = self._find_min(ask_orders.left)
        right_min = self._find_max(ask_orders.right)
        if left_min <= ask_orders:
            return left_min
        elif right_min <= ask_orders:
            return right_min
        return ask_orders

    def iterate(self):
        max_buy = self._find_max(self.orders["B"].root)
        min_ask = self._find_min(self.orders["S"].root)
        return max_buy, min_ask


class OrderIdLinearSearch(OrderBookIterator):
    def __init__(self, orders):
        self.orders = orders

    def iterate(self):
        pass