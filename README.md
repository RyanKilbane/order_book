# order_book
## Order
Inside `order.py` is a builder, `OrderBuilder` that does some basic validation on the incoming order string, the `build(self)` method constructs an `Order` object and returns that.

In the end I think I've managed the following:

Get best bid/ask: `O(ln(n))`
Update order: `O(1)`
Cancel order: `O(n)`

This was written using Python 3.8.5