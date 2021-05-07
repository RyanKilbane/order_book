from pytest import raises
from order_book.order.order import Order, OrderBuilder, InvalidAction, InvalidSize

def test_order_builder():
    order_builder = OrderBuilder()
    order_builder.set_action("a")
    order_builder.set_order_id("1234abcd")
    order_builder.set_price("123.03123")
    order_builder.set_side("B")
    order_builder.set_size("100")
    order_builder.set_ticker("ABCD")
    order_builder.set_time("123456789")
    order = order_builder.build()
    assert isinstance(order, Order)

def test_update_order():
    order_builder = OrderBuilder()
    order_builder.set_action("u")
    order_builder.set_order_id("1234abcd")
    order_builder.set_size(100)
    order = order_builder.build()
    assert isinstance(order, Order)

def test_order_invalid_action():
    order_builder = OrderBuilder()
    with raises(InvalidAction) as err:
        order_builder.set_action("G")

def test_order_invalid_size():
    order_builder = OrderBuilder()
    with raises(InvalidSize) as err:
        order_builder.set_size("0")
    with raises(InvalidSize) as err:
        order_builder.set_size("-1")
    with raises(InvalidSize) as err:
        order_builder.set_size("ABC")