# book
`book.py` contains the main objects of interest
## OrderBook
`OrderBook ` maintains three dictionaries for three different purposes, these dicts and their types are:
```python
self.tickers: Dict[str, TickerOrderBook]
self.ids: Dict[str, Order]
self.ticker_id_map: Dict[str, Set[Order]]
```
The first dict, maps a ticker string to it's corisponding OrderBook, ie. every ticker has a kind of sub order book that contains all orders involving that ticker. We'll have more to say on this later.

The seond dict, maps an order id directly to an `Order`. Since this map will point to the same order object that is placed in the `OrderTree,` this enables us to update an `Order` in `O(1)` time at the expense of some memory.

The third dict, maps a ticker to a set of `Order` objects. This should mean that it is realatively efficient to check if an Order id belongs to a certain ticker: We can check `x in set()` in `O(1)` time, which means checking if an arbitary `order_id` belongs to a certain ticker should be proportional to the number of tickers we have, ie checking which ticker an order id belongs to should happen in `O(N)` time.

### find_by
