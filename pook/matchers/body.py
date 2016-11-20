from .base import BaseMatcher


class BodyMatcher(BaseMatcher):

    @BaseMatcher.matcher
    def match(self, req):
        return True
