from pytest import raises
from order_book.process import make_order
from order_book.order.order import Order, OrderBuilder
from order_book.book.book import OrderBook, TickerOrderBook
from order_book.book.exceptions import NoTickerException

def test_add_new_order_book():
    order_book = OrderBook()
    incoming = "123456789|abbb111|a|AAPL|B|209.00000|100"
    order = make_order(incoming)
    order_book.insert(order)
    order_book.insert(order)
    order_book.insert(order)

def test_no_ticker_found():
    order_book = OrderBook()
    with raises(NoTickerException) as e:
        order_book["AAPL"]