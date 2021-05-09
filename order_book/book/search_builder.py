class InvalidTraversal(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidSearch(Exception):
    def __init__(self, message):
        super().__init__(message)


class SearchBuilder:
    def __init__(self):
        self.traversal_type = None
        self.search_type = None

    def add_traversal(self, traversal):
        try:
            self._validate_traversal(traversal)
            self.traversal_type = traversal
        except InvalidTraversal as e:
            raise e
        return self

    def _validate_traversal(self, traversal):
        valid_traversals = ["inorder", "preorder", "postorder"]
        if traversal not in valid_traversals:
            raise InvalidTraversal(f"The supplied traversal type is not supported, valid traversals are: {valid_traversals}")

    def add_search(self, search):
        try:
            self._validate_search(search)
            self.search_type = search
        except InvalidSearch as e:
            raise e
        return self

    def _validate_search(self, search):
        valid_searches = ["price", "order"]
        if search not in valid_searches:
            raise InvalidSearch(f"The supplied search type is invalid, valid searchs are: {valid_searches}")

    def build(self):
        return SearchParams(self)


class SearchParams:
    def __init__(self, search_builder: SearchBuilder):
        self.traversal_type = search_builder.traversal_type
        self.search_type = search_builder.search_type