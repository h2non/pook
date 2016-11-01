from .base import BaseMatcher


class JSONMatcher(BaseMatcher):
    def match(self, req):
        return True
