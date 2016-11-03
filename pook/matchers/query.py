import sys
from .base import BaseMatcher

if sys.version_info < (3,):     # Python 2
    from urlparse import urlparse, parse_qs
else:                           # Python 3
    from urllib.parse import urlparse, parse_qs


class QueryMatcher(BaseMatcher):
    def __init__(self, params):
        self.params = parse_qs(params)

    def match(self, req):
        return True
