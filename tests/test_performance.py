from order_book.process import build_book
from order_book.book.book import OrderBook

def test_performance():
    with open("/home/ryan/Documents/project-repos/order_book/test_data.txt", "r") as f:
        data =  f.readlines()
    book = OrderBook()
    for order in data:
        build_book(book, order)
    book.find_by("BFPP")

