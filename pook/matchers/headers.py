from .base import BaseMatcher


class HeadersMatcher(BaseMatcher):
    def __init__(self, headers):
        if not isinstance(headers, dict):
            raise TypeError('headers must be a dictionary')
        self.expectation = headers

    def match(self, req):
        return True
