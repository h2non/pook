from .base import BaseMatcher


class BodyMatcher(BaseMatcher):
    """
    BodyMatchers matches the request body via strict value comparison or
    regular expression based matching.
    """

    @BaseMatcher.matcher
    def match(self, req):
        expectation = self.expectation

        # Decode bytes input
        if isinstance(expectation, bytes):
            expectation = expectation.decode('utf-8')

        return self.compare(self.expectation, req.body)
