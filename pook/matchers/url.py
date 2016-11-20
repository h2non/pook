import sys
from .base import BaseMatcher
from .helpers import compare
from .path import PathMatcher
from .query import QueryMatcher

if sys.version_info < (3,):     # Python 2
    from urlparse import urlparse
else:                           # Python 3
    from urllib.parse import urlparse


class URLMatcher(BaseMatcher):
    """
    URLMatcher implements an URL schema matcher.
    """

    def __init__(self, url):
        if not url:
            raise ValueError('url argument cannot be empty')
        self.expectation = urlparse(url)

    def match_path(self, req):
        path = self.expectation.path
        if not path:
            return True
        return PathMatcher(path).match(req)

    def match_query(self, req):
        query = self.expectation.query
        if not query:
            return True
        return QueryMatcher(query).match(req)

    @BaseMatcher.matcher
    def match(self, req):
        url = self.expectation
        return all([
            compare(url.scheme, req.url.scheme),
            compare(url.hostname, req.url.hostname),
            compare(url.port, req.url.port),
            self.match_path(req),
            self.match_query(req)
        ])
