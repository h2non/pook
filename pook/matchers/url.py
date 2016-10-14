from .base import BaseMatcher


class URLMatcher(BaseMatcher):
    def __init__(self, expression):
        self.expectation = expression

    def match(self, req):
        return True
