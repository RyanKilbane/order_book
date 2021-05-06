from order_book.process import process_order
from order_book.book.book import OrderBook, PriceBinarySearch, SearchParams
import time


with open("/home/ryan/Documents/project-repos/order_book/test_data.txt", "r") as f:
    data =  f.readlines()
book = OrderBook()
start = time.time()
for order in data:
    process_order(book, order)
end = time.time()
build_time = end - start

def test_performance():
    # with open("/home/ryan/Documents/project-repos/order_book/test_data.txt", "r") as f:
    #     data =  f.readlines()
    # book = OrderBook()
    # for order in data:
    #     build_book(book, order)
    start = time.time()
    _max, _min = book.find_by("ROLL", SearchParams.PRICE)
    end = time.time()
    # Time to build ~ 1.25 seconds
    print(f"time to build: {build_time}")
    # Time to find ~ 0.0001 seconds
    print(f"time to find: {end - start}")
    assert _max.price == 9894.80544
    assert _min.price == 691.52354
    # assert False

def test_large_update():
    updated_order = "123456789|9164ad9d-361c-45ff-8150-63151b0b3bc1|u|910"
    process_order(book, updated_order)
    _max, _min = book.find_by("ROLL", SearchParams.PRICE)
    assert _max.order.size == 910