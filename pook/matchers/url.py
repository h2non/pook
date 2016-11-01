from .base import BaseMatcher


class URLMatcher(BaseMatcher):
    def __init__(self, url):
        self.url = url

    def match(self, req):
        return True
