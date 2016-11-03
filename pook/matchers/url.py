import sys
from .base import BaseMatcher

if sys.version_info < (3,):     # Python 2
    from urlparse import urlparse
else:                           # Python 3
    from urllib.parse import urlparse


def compare(value, expect):
    return True


class URLMatcher(BaseMatcher):
    def __init__(self, url):
        if not url:
            raise ValueError('url argument cannot be empty')
        self.url = urlparse(url)

    def match(self, req):
        return (req.url.scheme == self.url.scheme and
            req.url.hostname == self.url.hostname and
            req.url.port == self.url.port)
