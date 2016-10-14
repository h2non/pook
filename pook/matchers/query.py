from .base import BaseMatcher


class QueryMatcher(BaseMatcher):
    def __init__(self, params):
        self.expectation = params

    def match(self, req):
        return True
