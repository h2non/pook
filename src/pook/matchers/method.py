from .base import BaseMatcher


class MethodMatcher(BaseMatcher):
    """
    MethodMatcher implements.
    """

    @BaseMatcher.matcher
    def match(self, req):
        return (self.expectation == '*' or
                self.compare(req.method.lower(), self.expectation.lower()))
