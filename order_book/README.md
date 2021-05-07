# process
Main driver methods.
## process_order
Takes an `OrderBook` object and a string of data, first builds an `Order` object and will then either insert, update or cancel based on the `Order.action` attribute.

## get_best_buy_ask
Takes an `OrderBook` object and ticker string. Does binary search on `OrderTree` objects and returns the largest bid order and the smallest ask order. Returns bid, ask `Order` objects.