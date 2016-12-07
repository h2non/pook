from .base import BaseMatcher


class BodyMatcher(BaseMatcher):
    """
    BodyMatchers matches the request body via strict value comparison or
    regular expression based matching.
    """

    @BaseMatcher.matcher
    def match(self, req):
        return self.compare(self.expectation, req.body)
