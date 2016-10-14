from .base import BaseMatcher


class MethodMatcher(BaseMatcher):
    def __init__(self, method):
        self.expectation = method

    def match(self, req):
        return self.expectation == '*' or req.expectation == self.method
