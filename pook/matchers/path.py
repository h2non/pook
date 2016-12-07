from .base import BaseMatcher


class PathMatcher(BaseMatcher):
    """
    PathMatcher implements an URL path matcher.
    """

    @BaseMatcher.matcher
    def match(self, req):
        return self.compare(self.expectation, req.url.path)
