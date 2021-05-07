class InvalidAction(Exception):
    def __init__(self, message):
        super().__init__(message)

class InvalidSide(Exception):
    def __init__(self, message):
        super().__init__(message)

class InvalidSize(Exception):
    def __init__(self, message):
        super().__init__(message)

class InvalidPrice(Exception):
    def __init__(self, message):
        super().__init__(message)


class OrderBuilder:
    def __init__(self):
        self.time_stamp = None
        self.order_id = None
        self.action = None
        self.ticker = None
        self.side = None
        self.price = None
        self.size = None
    
    def set_time(self, time):
        self.time_stamp = time
        return self

    def set_order_id(self, oid):
        self.order_id = oid
        return self

    def set_action(self, action):
        try:
            self._validate_action(action)
            self.action = action
        except InvalidAction as e:
            raise e
        return self

    def _validate_action(self, action):
        # potential micro optimisation is to remove this
        # it's almost certainly not needed
        valid_actions = ["a", "u", "c"]
        if action not in valid_actions:
            raise InvalidAction(f"An action was recived that shouldn't have been recived. Expected: {valid_actions} Got: {action}")

    def set_ticker(self, ticker):
        self.ticker = ticker
        return self

    def set_side(self, side):
        try:
            self._validate_side(side)
            self.side = side
        except InvalidSide as e:
            raise e
        return self

    def _validate_side(self, side):
        valid_sides = ["B", "S"]
        if side not in valid_sides:
            raise InvalidSide(f"Side can only take on values B and S, got: {side}")

    def set_price(self, price):
        # WARNING: potential loss of precision here, would it matter if
        # float(123.00000) -> 123.0?
        # Might switch to decimal to maintain arbitary precision
        self.price = float(price)
        return self

    def set_size(self, size):
        try:
            self._validate_size(size)
            self.size = int(size)
        except InvalidSize as e:
            raise e
        
    def _validate_size(self, size):
        # First ensure size is an int
        try:
            int(size)
        except ValueError:
            raise InvalidSize("Could not convert given size to an integer")
        
        if int(size) <= 0:
            raise InvalidSize("Size can not be less than zero")

    def build(self):
        return Order(self)

class Order:
    def __init__(self, order_builder: OrderBuilder):
        self.time_stamp = order_builder.time_stamp
        self.order_id = order_builder.order_id
        self.action = order_builder.action
        self.ticker = order_builder.ticker
        self.side = order_builder.side
        self.price = order_builder.price
        self.size = order_builder.size

    def __str__(self):
        return f"{self.time_stamp}|{self.order_id}|{self.action}|{self.ticker}|{self.side}|{self.price}|{self.size}"