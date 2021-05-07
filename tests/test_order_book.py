from pytest import raises
from order_book.process import make_order
from order_book.order.order import Order, OrderBuilder
from order_book.book.book import OrderBook, SearchParams, TickerOrderBook
from order_book.book.exceptions import NoTickerException
from order_book.book.book_iterators import TraversalTypes

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

def test_cancel_order():
    order_book = OrderBook()
    incoming = "123456789|aab123|a|AAPL|B|209.00000|100"
    order = make_order(incoming)
    incoming = "123456789|aab124|a|AAPL|B|109.00000|100"
    lower_order = make_order(incoming)
    incoming = "123456789|aab125|a|AAPL|B|250.00000|100"
    higher_order = make_order(incoming)
    incoming = "123456789|aab126|a|AAPL|B|150.00000|100"
    fifth_order = make_order(incoming)
    incoming = "123456789|aab127|a|AAPL|S|150.00000|100"
    fourth_order = make_order(incoming)
    order_book.insert(order)
    order_book.insert(lower_order)
    order_book.insert(higher_order)
    order_book.insert(fourth_order)
    order_book.insert(fifth_order)
    # We're going to cancel order aab125
    # First make sure it's in the tree
    bid, ask = order_book.find_by("AAPL", SearchParams.ORDER, traversal=TraversalTypes.INORDER)
    oids = [i.order.order_id for i in bid]
    assert "aab125" in oids
    order_book.cancel_order(higher_order)
    # Now order aab125 should have been canceled
    # So lets traverse the tree
    bid, ask = order_book.find_by("AAPL", SearchParams.ORDER, traversal=TraversalTypes.INORDER)
    oids = [i.order.order_id for i in bid]
    # Now aab125 SHOULD NOT be in oids
    assert "aab125" not in oids


def test_raises_no_ticker_exception():
    order_book = OrderBook()
    with raises(NoTickerException) as e:
        order_book.find_by("AAPL", SearchParams.ORDER, traversal=TraversalTypes.INORDER)