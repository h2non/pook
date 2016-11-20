from .base import BaseMatcher


class JSONMatcher(BaseMatcher):
    """
    JSONMatcher implements a query matcher.
    """

    @BaseMatcher.matcher
    def match(self, req):
        return True
