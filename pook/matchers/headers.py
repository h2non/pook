from .base import BaseMatcher


class HeadersMatcher(BaseMatcher):
    def __init__(self, headers):
        if not isinstance(headers, dict):
            raise TypeError('headers must be a dictionary')
        self.expectation = headers

    def match(self, req):
        for key, value in self.expectation.items():
            header = req.headers.get(key)
            if not header:
                return False
            if not self.match_regexp(value, header) or header != value:
                return False
        return True
