from order_book.process import make_order
from order_book.order.order import Order, OrderBuilder
from order_book.book.book import OrderBook, TickerOrderBook

def test_add_new_order_book():
    order_book = OrderBook()
    incoming = "123456789|abbb111|a|AAPL|B|209.00000|100"
    order = make_order(incoming)
    order_book.add_new_order(order)
    order_book.add_new_order(order)
    order_book.add_new_order(order)
    assert "AAPL" in order_book.tickers
    assert isinstance(order_book["AAPL"], TickerOrderBook)
    assert order_book["AAPL"].orders["B"][0] == order
    assert len(order_book["AAPL"].orders["B"]) == 3

def test_add_new_ask_order_book():
    order_book = OrderBook()
    incoming = "123456789|abbb111|a|AAPL|S|209.00000|100"
    order = make_order(incoming)
    order_book.add_new_order(order)
    assert "AAPL" in order_book.tickers
    assert isinstance(order_book["AAPL"], TickerOrderBook)
    assert order_book["AAPL"].orders["S"][0] == order
    assert len(order_book["AAPL"].orders["S"]) == 1

