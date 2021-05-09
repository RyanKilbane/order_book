from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict

from order_book.book.search_builder import SearchParams

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

    def iterate(self, search_params):
        max_bid = self._find_max(self.orders["B"].root)
        min_ask = self._find_min(self.orders["S"].root)
        return max_bid, min_ask


class OrderIdSearch(OrderBookIterator):
    def __init__(self, orders):
        self.orders = orders

    def _traversal_factory(self, taversal_type):
        traverse = {"inorder": InorderTraversal,
                    "preorder": PreorderTraversal,
                    "postorder": PostorderTraversal}
        return traverse[taversal_type]

    def iterate(self, search_params: SearchParams):
        traversal_type = search_params.traversal_type
        walker = self._traversal_factory(traversal_type)(self.orders)
        return walker.iterate()

class InorderTraversal(OrderBookIterator):
    def __init__(self, order):
        self.orders = order
        self.arr = []

    def _inorder(self, node):
        if node:
            self._inorder(node.left)
            self.arr.append(node)
            self._inorder(node.right)

    def iterate(self):
        # traverse bids
        self._inorder(self.orders["B"].root)
        bids = self.arr
        # Reset array
        self.arr = []
        # traverse asks
        asks = self._inorder(self.orders["S"].root)
        asks = self.arr
        return bids, asks


class PreorderTraversal(OrderBookIterator):
    def __init__(self, order):
        self.orders = order
        self.arr = []
    
    def _preorder(self, node):
        if node.left is not None:
            self.arr.append(node.left.order.order_id)
            left = self._preorder(node.left)
        if node.right is not None:
            self.arr.append(node.right.order.order_id)
            right = self._preorder(node.right)

    def iterate(self):
        self.arr.append(self.orders["B"].root.order.order_id)
        bid = self._preorder(self.orders["B"].root)
        return self.arr

class PostorderTraversal(OrderBookIterator):
    def __init__(self, order):
        self.orders = order
    
    def iterate(self):
        raise NotImplementedError("Postorder traversal has yet to be implemented")
