import re
import sys
from .base import BaseMatcher
from .path import PathMatcher
from .query import QueryMatcher
from ..regex import isregex

if sys.version_info < (3,):     # Python 2
    from urlparse import urlparse
else:                           # Python 3
    from urllib.parse import urlparse

# URI protocol test regular expression
protoregex = re.compile('^http[s]?://', re.IGNORECASE)


class URLMatcher(BaseMatcher):
    """
    URLMatcher implements an URL schema matcher.
    """

    # Matches URL as regular expression
    regex = False

    def __init__(self, url):
        if not url:
            raise ValueError('url argument cannot be empty')

        # Store original URL value
        self.url = url

        # Process as regex value
        if isregex(url):
            self.regex = True
            self.expectation = url
        else:
            # Add protocol prefix in the URL
            if not protoregex.match(url):
                self.url = 'http://{}'.format(url)
            self.expectation = urlparse(self.url)

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

        # Match as regex
        if self.regex:
            return self.compare(url, req.url.geturl(), regex_expr=True)

        # Match URL
        return all([
            self.compare(url.scheme, req.url.scheme),
            self.compare(url.hostname, req.url.hostname),
            self.compare(url.port or req.url.port, req.url.port),
            self.match_path(req),
            self.match_query(req)
        ])

    def __str__(self):
        return self.url

    def __repr__(self):
        return '{}({})'.format(self.name, self.url)
