from .base import BaseMatcher


class BodyMatcher(BaseMatcher):
    def match(self, req):
        return True
