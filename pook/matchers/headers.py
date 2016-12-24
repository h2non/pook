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
        for key in self.expectation:
            # Retrieve value to match
            value = self.expectation[key]

            # Retrieve header value by key
            header = req.headers.get(key)

            # Compare header value
            print('Match:', self.compare(value, header, regex_expr=True))
            if not self.compare(value, header, regex_expr=True):
                return False

        return True
