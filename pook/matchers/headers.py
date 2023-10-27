from .base import BaseMatcher
from ..headers import to_string_value


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
            # Cast it to a string that can be compared
            # If it is already a string ``to_string_value`` is a noop
            value = to_string_value(self.expectation[key])

            # Retrieve header value by key
            header = req.headers.get(key)

            # Compare header value
            if not self.compare(value, header, regex_expr=True):
                return False

        return True
