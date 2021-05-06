from order_book.book.book import OrderNode
from order_book.process import make_order

def test_overloads():
    incoming = "123456789|abbb111|a|AAPL|B|209.00000|100"
    order = make_order(incoming)
    on = OrderNode(order)
    assert on == 209.0
    assert on <= 209.0
    assert on <= 300
    assert on >= 100
    assert on != 100