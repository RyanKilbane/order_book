from order_book.process import make_order, get_best_bid_ask, OrderBook, process_order
from order_book.order.order import Order, OrderBuilder

def test_add_order():
    incoming = "123456789|abbb111|a|AAPL|B|209.00000|100"
    dummy_builder = OrderBuilder()
    order = Order(dummy_builder)
    order.time_stamp = "123456789"
    order.order_id = "abbb111"
    order.action = "a"
    order.ticker = "AAPL"
    order.side = "B"
    order.price = 209.0
    order.size = 100
    new_order = make_order(incoming)
    assert new_order.time_stamp == order.time_stamp
    assert new_order.order_id == order.order_id
    assert new_order.action == order.action
    assert new_order.ticker == order.ticker
    assert new_order.side == order.side
    assert new_order.price == order.price
    assert new_order.size == order.size

def test_get_bid_ask():
    book = OrderBook()
    incoming = "123456789|abbb111|a|AAPL|B|209.00000|100"
    process_order(book, incoming)
    incoming = "123456789|abbb112|a|AAPL|S|10.00000|100"
    process_order(book, incoming)
    bid, ask = get_best_bid_ask(book, "AAPL")
    assert bid == 209.00000
    assert ask == 10.00000