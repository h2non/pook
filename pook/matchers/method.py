from .base import BaseMatcher


class MethodMatcher(BaseMatcher):
    def match(self, req):
        return (self.expectation == '*' or
                req.method.lower() == self.expectation.lower())
