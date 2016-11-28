from .base import BaseMatcher
from .compare import compare


class PathMatcher(BaseMatcher):
    """
    PathMatcher implements an URL path matcher.
    """

    @BaseMatcher.matcher
    def match(self, req):
        return compare(self.expectation, req.url.path)
