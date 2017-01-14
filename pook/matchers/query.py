import sys
from .base import BaseMatcher

if sys.version_info < (3,):     # Python 2
    from urlparse import parse_qs
else:                           # Python 3
    from urllib.parse import parse_qs


class QueryMatcher(BaseMatcher):
    """
    QueryMatcher implements an URL query params matcher.
    """

    def match_query(self, query, req_query):
        def test(key, param):
            match = req_query.get(key)
            if match is None:
                return False

            # Normalize param value
            param = [param] if not isinstance(param, list) else param

            # Compare query params
            [[self.compare(value, expect)
              for expect in match] for value in param]

            return True

        return all([test(key, query[key]) for key in query])

    @BaseMatcher.matcher
    def match(self, req):
        query = self.expectation

        # Parse and assert type
        if isinstance(query, str):
            query = parse_qs(self.expectation)

        # Validate query params
        if not isinstance(query, dict):
            raise ValueError('query params must be a str or dict')

        # Parse request URL query
        req_query = parse_qs(req.url.query)

        # Match query params
        return self.match_query(query, req_query)
