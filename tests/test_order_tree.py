from order_book.book.book import OrderBook, OrderNode, OrderTree, TickerOrderBook
from order_book.process import make_order
from order_book.order.order import Order

def test_overloads():
    incoming = "123456789|abbb111|a|AAPL|B|209.00000|100"
    order = make_order(incoming)
    on = OrderNode(order)
    assert on == 209.0
    assert on <= 209.0
    assert on <= 300
    assert on >= 100
    assert on != 100

def test_one_insert():
    incoming = "123456789|abbb111|a|AAPL|B|209.00000|100"
    order = make_order(incoming)
    order_tree = OrderTree()
    order_tree.insert(order)
    assert order_tree.root.order == order

def test_two_insert():
    incoming = "123456789|abbb111|a|AAPL|B|209.00000|100"
    order = make_order(incoming)
    incoming = "123456789|abbb111|a|AAPL|B|109.00000|100"
    lower_order = make_order(incoming)
    order_tree = OrderTree()
    order_tree.insert(order)
    order_tree.insert(lower_order)
    assert order_tree.root.order == order
    assert order_tree.root.left.order == lower_order 

def test_three_insert():
    incoming = "123456789|abbb111|a|AAPL|B|209.00000|100"
    order = make_order(incoming)
    incoming = "123456789|abbb111|a|AAPL|B|109.00000|100"
    lower_order = make_order(incoming)
    incoming = "123456789|abbb111|a|AAPL|B|250.00000|100"
    higher_order = make_order(incoming)
    order_tree = OrderTree()
    order_tree.insert(order)
    order_tree.insert(lower_order)
    order_tree.insert(higher_order)
    assert order_tree.root.order == order
    assert order_tree.root.left.order == lower_order 
    assert order_tree.root.right.order == higher_order

def test_four_insert():
    incoming = "123456789|abbb111|a|AAPL|B|209.00000|100"
    order = make_order(incoming)
    incoming = "123456789|abbb111|a|AAPL|B|109.00000|100"
    lower_order = make_order(incoming)
    incoming = "123456789|abbb111|a|AAPL|B|250.00000|100"
    higher_order = make_order(incoming)
    incoming = "123456789|abbb111|a|AAPL|B|150.00000|100"
    fourth_order = make_order(incoming)
    order_tree = OrderTree()
    order_tree.insert(order)
    order_tree.insert(lower_order)
    order_tree.insert(higher_order)
    order_tree.insert(fourth_order)
    assert order_tree.root.order == order
    assert order_tree.root.left.order == lower_order 
    assert order_tree.root.right.order == higher_order
    assert order_tree.root.left.right.order == fourth_order

def test_constant_update():
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
    # Update an order
    updated_order = make_order("123456789|aab125|a|AAPL|B|250.00000|10")
    order_book.update_order(updated_order)
    # get ticker
    ticker_book: TickerOrderBook = order_book["AAPL"]
    buy_orders: OrderTree = ticker_book["B"]
    updated_order: Order = buy_orders.root.right.order
    assert updated_order.size == 10
    
def test_constant_cancel():
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
    # Update an order
    updated_order = make_order("123456789|aab125|c|AAPL|B|250.00000|100")
    order_book.cancel_order(updated_order)
    # get ticker
    ticker_book: TickerOrderBook = order_book["AAPL"]
    buy_orders: OrderTree = ticker_book["B"]
    updated_order: Order = buy_orders.root.right.order
    assert updated_order.action == "c"

def test_find_max():
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
    buy_max, ask_min = order_book.find_by("AAPL")
    assert buy_max == 250

def test_find_min():
    order_book = OrderBook()
    incoming = "123456789|aab123|a|AAPL|S|209.00000|100"
    order = make_order(incoming)
    incoming = "123456789|aab124|a|AAPL|S|109.00000|100"
    lower_order = make_order(incoming)
    incoming = "123456789|aab125|a|AAPL|S|250.00000|100"
    higher_order = make_order(incoming)
    incoming = "123456789|aab126|a|AAPL|S|150.00000|100"
    fourth_order = make_order(incoming)
    order_book.insert(order)
    order_book.insert(lower_order)
    order_book.insert(higher_order)
    order_book.insert(fourth_order)
    buy_max, ask_min = order_book.find_by("AAPL")
    assert ask_min == 109