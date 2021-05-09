from order_book.book.book_iterators import OrderIdSearch
from order_book.book.book import OrderBook, SearchParams
from order_book.process import make_order
from order_book.book.search_builder import SearchBuilder

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
    search_params = SearchBuilder().add_search("order").add_traversal("preorder")
    x = order_book.find_by("AAPL", search_params)
    assert ["aab123", "aab124", "aab126", "aab125"] == x

def test_inorder_traversal():
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
    search_params = SearchBuilder().add_search("order").add_traversal("inorder").build()
    bids, ask = order_book.find_by("AAPL", search_params)
    print(bids)
    oids = [i.order.order_id for i in bids]
    # assert ["aab124", "aab126", "aab123", "aab125"] == oids
    assert len(oids) == 4
    assert oids[0] == "aab124"
    assert oids[1] == "aab126"
    assert oids[2] == "aab123"
    assert oids[3] == "aab125"