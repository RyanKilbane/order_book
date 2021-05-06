from abc import ABC, AbstractMethod
from enum import Enum
from typing import Dict

class Book(ABC):
    @AbstractMethod
    def find_by():
        pass

class BookIterator(ABC):
    @AbstractMethod
    def iterate():
        pass

class OrderBook(ABC):
    def __init__(self):
        self.tickers: Dict[str, TickerOrderBook] = {}

    def add_new_order(self, order):
        if order.ticker not in self.tickers:
            tob = TickerOrderBook()
            tob.add(order)
            self.tickers[order.ticker] = tob
        self.tickers[order.ticker].add(order)

    def __getitem__(self, ticker):
        return self.tickers[ticker]

    def find_by(self, ticker, by_clause):
        '''
        Take param and search ticker by that clause
        '''
        return self.tickers[ticker].find_by(by_clause)


class TickerOrderBook(ABC):
    def __init__(self):
        self.orders = []

    def add(self, order):
        # do binary search here find the correct place to slot in the new order.
        # This should be better than re-sorting on every add ie. O(ln(N)) VS O(Nln(N))
        self.order.append(order)
    
    def find_by(self, by_clause):
        if by_clause is SearchParams.MAX:
            # The max value should always be the last element
            return self.orders[-1]
        elif by_clause is SearchParams.MIN:
            # The min value should always be the first element
            return self.orders[0]

    def _find_by_max(self):
        pass

    def _find_by_min(self):
        pass


class OrderBookIterator(BookIterator):
    pass


class SearchParams(Enum):
    MAX = 1
    MIN = 2
    OTHER = 3