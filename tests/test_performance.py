from order_book.process import build_book
from order_book.book.book import OrderBook
import time


with open("/home/ryan/Documents/project-repos/order_book/test_data.txt", "r") as f:
    data =  f.readlines()
book = OrderBook()
start = time.time()
for order in data:
    build_book(book, order)
end = time.time()
build_time = end - start

def test_performance():
    # with open("/home/ryan/Documents/project-repos/order_book/test_data.txt", "r") as f:
    #     data =  f.readlines()
    # book = OrderBook()
    # for order in data:
    #     build_book(book, order)
    start = time.time()
    _max, _min = book.find_by("BFPP")
    end = time.time()
    # Time to build ~ 1.25 seconds
    print(f"time to build: {build_time}")
    # Time to find ~ 0.0001 seconds
    print(f"time to find: {end - start}")
    assert _max.price == 9895.97896
    assert _min.price == 746.34318
    # assert False

def test_large_update():
    updated_order = "123456789|e114a4a6-28d1-4b13-8dca-70c8f9cc1bba|u|910"
    build_book(book, updated_order)
    _max, _min = book.find_by("BFPP")
    assert _max.order.size == 910