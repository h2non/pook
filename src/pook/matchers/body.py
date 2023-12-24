from .base import BaseMatcher


class BodyMatcher(BaseMatcher):
    """
    BodyMatchers matches the request body via strict value comparison or
    regular expression based matching.
    """

    def __init__(self, *args, **kwargs):
        self.binary = kwargs.pop("binary", False)
        super().__init__(*args, **kwargs)

    @BaseMatcher.matcher
    def match(self, req):
        expectation = self.expectation

        # Decode bytes input
        if isinstance(expectation, bytes) and not self.binary:
            expectation = expectation.decode("utf-8")

        return self.compare(self.expectation, req.body)
