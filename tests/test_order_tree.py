from order_book.book.book import OrderNode, OrderTree
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