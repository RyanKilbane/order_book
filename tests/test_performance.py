from order_book.process import process_order
from order_book.book.book import OrderBook, PriceBinarySearch, SearchParams
from order_book.book.search_builder import SearchBuilder
import time
import pytest

#pytestmark = pytest.mark.skip(reason="relatively long tests that require generation of test data")
'''
If you want to run these tests, first generate some test data using tests/resources/generate_test_data.py
'''
with open("/home/ryan/Documents/project-repos/order_book/test_data.txt", "r") as f:
    data =  f.readlines()
book = OrderBook()
start = time.time()
for order in data:
    process_order(book, order)
end = time.time()
build_time = end - start

def test_performance():
    search_params = SearchBuilder().add_search("price").build()
    start = time.time()
    _max, _min = book.find_by("KPXJ", search_params)
    end = time.time()
    # Time to build ~ 1.25 seconds
    print(f"time to build: {build_time}")
    # Time to find ~ 0.0001 seconds
    print(f"time to find: {end - start}")
    assert _max.price == 9829.53242
    assert _min.price == 149.65574
    # assert False

def test_large_update():
    # Original order: 123456789|0c67a6f6-95a1-4c83-8f3c-ba1c5ad3998f|a|KPXJ|B|9829.53242|745
    updated_order = "123456789|0c67a6f6-95a1-4c83-8f3c-ba1c5ad3998f|u|910"
    process_order(book, updated_order)
    search_type = SearchBuilder().add_search("price").build()
    _max, _min = book.find_by("KPXJ", search_type)
    assert _max.order.size == 910

def test_large_cancel():
    cancel_order = "123456789|0c67a6f6-95a1-4c83-8f3c-ba1c5ad3998f|c"
    start = time.time()
    process_order(book, cancel_order)
    end = time.time()
    # Time to cancel ~ 0.001 s
    print(f"cancelation: {end - start}")
    # assert False