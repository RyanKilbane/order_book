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

The third dict, maps a ticker to a set of `Order` objects. This should mean that it is relatively efficient to check if an Order id belongs to a certain ticker: We can check `x in set()` in `O(1)` time, which means checking if an arbitary `order_id` belongs to a certain ticker should be proportional to the number of tickers we have, ie checking which ticker an order id belongs to should happen in `O(N)` time. This is used for canceling an order.

### insert
Creates a new `TickerOrderBook` and adds that to the `self.tickers` dictionary. Initalises the `self.ids` dict and `self.ticker_id_map`. Calls `insert` on `TickerOrderBook`

### find_by
Interface to `find_by` in `OrderTree`. `search_type` is an Enum of two elements:
```python
class SearchTypes:
    PRICE = 1
    ORDER = 2
```
The `PRICE` enum is passed when wanting to search by price (in the current limited implementation, this just finds max and min prices). `ORDER` enum is passed when you want to search by order_id. When searching by order_id, a further parameter, `traverse` will need to be passed, this is also an enum:
```python
class TraversalTypes:
    INORDER = 1
    PREORDER = 2
    POSTORDER = 3
```
### update_order
Method to update orders, takes an `order_id` and looks up the coresponding `Order` object in the `self.id`, then updates the `size` field. Since both `self.id` and `OrderNode` point to the same object, updating the object in the dict should update the `OrderNode`. This means we should be able to update an order in `O(1)`
### cancel_order
Mostly just an interface to `TickerOrderBook.cancel_order()`, calls `_find_ticker_from_order_id` to find which ticker an order_id belongs to.
### _find_ticker_from_order_id
Iterates over the `ticker_id_map` then checks if `order_id` is in the coresponding `set` of order_ids. Since Python set's are hash sets, look-ups should be `O(1)`. Which means that looking up an order_id should be linear in the number of tickers.

## TickerOrderBook
Each ticker has it's own order book, which in turn splits it's orders into two seperate `OrderTree`'s one of bid and another for ask.

### insert
Interface to the `OrderTree` interface method.

### cancel_order
cancel_order doesn't really cancel an order, it instead rebuilds the entire tree _without_ the order with the corisponding order_id. This is an unfortunate consequence of me not really knowing what assumptions I could make about the order_id, I don't think there's any better way of dealing with search by order_id in general than an `O(1)` search. There are a couple of ideas (creating an auxiliary tree and perhaps using a hash of order_id to create a key, but that has it's own problems.)

### find_by
Takes the same parameters as the previous `find_by`. This time it calls a factory function, which returns the Iterator class.

### _search_factory
Takes a `SearchTypes` enum and returns an uninitialised class that serves as an interface to the iterators.

## OrderNode
Just a data object with some operator overloading.

# book_iterators
Module containing iterators for the `OrderTree` class.
## PriceBinarySearch
Does exactly what it says on the tin, it searches the `OrderTree` looking for either the maximum or minimum price.

## OrderIdSearch
Really just an interface to some tree traversal classes.

### _traversal_factory
Based on the `traversal` argument returns an unintialised class that is one of: `InorderTraversal`, `PreorderTraversal`, or `PostOrderTraversal`. The class is then instantiated in the `iterate` method and `self.orders` is passed. `self.orders` here is a dictionary that looks like:
```python
self.orders = {"B": OrderTree(), "S": OrderTree()}
```