from .base import BaseMatcher


class HeadersMatcher(BaseMatcher):
    """
    Headers HTTP request matcher.
    """

    def __init__(self, headers):
        if not isinstance(headers, dict):
            raise TypeError('headers must be a dictionary')
        BaseMatcher.__init__(self, headers)

    @BaseMatcher.matcher
    def match(self, req):
        for key, value in self.expectation.items():
            header = req.headers.get(key)

            if not header:
                return False

            if not self.match_regexp(value, header) or header != value:
                return False

        return True
