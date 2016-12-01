from ..types import isregex
from .base import BaseMatcher
from .compare import compare


class BodyMatcher(BaseMatcher):
    """
    BodyMatchers matches the request body via strict value comparison or
    regular expression based matching.
    """

    @BaseMatcher.matcher
    def match(self, req):
        body = req.body

        if body == self.expectation:
            return True

        if isregex(self.expectation):
            return self.expectation.match(body or '') is not None

        if not body and self.expectation:
            return False

        if not isinstance(body, str):
            return False

        return self.compare(self.expectation, body)
