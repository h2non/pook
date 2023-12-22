import re

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
            value = self.to_comparable_value(self.expectation[key])

            # Retrieve header value by key
            header = req.headers.get(key)

            # Compare header value
            if not self.compare(value, header, regex_expr=True):
                return False

        return True

    def to_comparable_value(self, value):
        """
        Return a comparable version of ``value``.

        Arguments:
            value (mixed): the value to cast.

        Returns:
            str|re.Pattern|None
        """
        if isinstance(value, (str, re.Pattern)):
            return value

        if value is None:
            return value

        return to_string_value(value)
