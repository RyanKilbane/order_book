from order_book.book.book_iterators import OrderIdSearch, TraversalTypes
from order_book.book.book import OrderBook, SearchParams
from order_book.process import make_order

def test_preorder_traversal():
    order_book = OrderBook()
    incoming = "123456789|aab123|a|AAPL|B|209.00000|100"
    order = make_order(incoming)
    incoming = "123456789|aab124|a|AAPL|B|109.00000|100"
    lower_order = make_order(incoming)
    incoming = "123456789|aab125|a|AAPL|B|250.00000|100"
    higher_order = make_order(incoming)
    incoming = "123456789|aab126|a|AAPL|B|150.00000|100"
    fourth_order = make_order(incoming)
    order_book.insert(order)
    order_book.insert(lower_order)
    order_book.insert(higher_order)
    order_book.insert(fourth_order)
    x = order_book.find_by("AAPL", SearchParams.ORDER, traversal=TraversalTypes.PREORDER)
    assert ["aab123", "aab124", "aab126", "aab125"] == x