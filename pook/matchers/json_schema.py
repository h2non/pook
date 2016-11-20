from .base import BaseMatcher


class JSONSchemaMatcher(BaseMatcher):
    """
    JSONSchema HTTP request body matcher.
    """

    @BaseMatcher.matcher
    def match(self, req):
        return True
