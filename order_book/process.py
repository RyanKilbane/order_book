from order_book.order.order import OrderBuilder, Order
from order_book.book.book import OrderBook

def make_order(incoming_string: str) -> Order:
    order = incoming_string.split("|")
    new_order = OrderBuilder()
    if order[2] == "a":
        # Add new order requires all fields
        new_order.set_time(order[0]).set_order_id(order[1]).set_action(order[2])\
                      .set_ticker(order[3]).set_side(order[4]).set_price(order[5]).set_size(order[6])
    elif order[2] == "u":
        # updates only require a subset
        new_order.set_time(order[0]).set_order_id(order[1]).set_action(order[2]).set_size(order[3])
    else:
        # cancelations again only require a subset
        new_order.set_time(order[0]).set_order_id(order[1]).set_action(order[2])

    return new_order.build()

def process_order(book: OrderBook, data):
    order = make_order(data)
    if order.action == "a":
        book.insert(order)
    elif order.action == "u":
        book.update_order(order)
    else:
        book.cancel_order(order)
