from ..headers import to_string_value
from ..regex import Pattern
from .base import BaseMatcher, ExistsMatcher


class HeadersMatcher(BaseMatcher):
    """
    Headers HTTP request matcher.
    """

    def __init__(self, headers):
        if not isinstance(headers, dict):
            raise TypeError("headers must be a dictionary")
        BaseMatcher.__init__(self, headers)

    @BaseMatcher.matcher
    def match(self, req):
        for key in self.expectation:
            assert key in req.headers, f"Header '{key}' not present"

            expected_value = self.to_comparable_value(self.expectation[key])

            # Retrieve header value by key
            actual_value = req.headers.get(key)

            assert not all(
                [
                    expected_value is not None,
                    actual_value is None,
                ]
            ), f"Expected a value `{expected_value}` " f"for '{key}' but found `None`"

            # Compare header value
            if not self.compare(expected_value, actual_value, regex_expr=True):
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
        if isinstance(value, (str, Pattern)):
            return value

        if value is None:
            return value

        return to_string_value(value)


class HeaderExistsMatcher(ExistsMatcher):
    request_attr = "headers"
