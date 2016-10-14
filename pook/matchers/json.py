from .base import BaseMatcher


class JSONBodyMatcher(BaseMatcher):
    def __init__(self, headers):
        self.expectation = headers

    def match(self, req):
        return True
