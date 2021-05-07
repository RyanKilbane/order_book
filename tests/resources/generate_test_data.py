import random
import string
import uuid

random.seed(1031)
uuid.UUID(int=random.getrandbits(124))
tickers = [''.join(random.choices(string.ascii_uppercase, k=4)) for i in range(1000)]

def gen_test_data():
    data = [["123456789",
             str(uuid.UUID(int=random.getrandbits(124), version=4)),
             "a",
             random.choice(tickers),
             random.choice(["B", "S"]),
             "{:.5f}".format(random.uniform(10, 10000)),
             str(random.randint(1, 1000))] for _ in range(10**5)]
    x = "\n".join('|'.join(i) for i in data)
    with open("/home/ryan/Documents/project-repos/order_book/test_data.txt", "w") as f:
        f.write(x)

gen_test_data()