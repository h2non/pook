from urllib.parse import parse_qs

from .base import BaseMatcher, ExistsMatcher


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
            [[self.compare(value, expect) for expect in match] for value in param]

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
            raise ValueError("query params must be a str or dict")

        # Parse request URL query
        req_query = parse_qs(req.url.query)

        # Match query params
        return self.match_query(query, req_query)


class QueryParameterExistsMatcher(ExistsMatcher):
    request_attr = "query"

    def __init__(self, expectation, allow_empty, negate=False):
        super().__init__(expectation, negate)
        self.allow_empty = allow_empty

    def match(self, request):
        if not super().match(request):
            return False

        if not self.allow_empty:
            attribute = self.get_request_attribute(request)
            assert not self.is_empty(
                attribute[self.expectation]
            ), f"The request's {self.expectation} query parameter was unexpectedly empty."

        return True

    def is_empty(self, value):
        """
        Check for empty query parameter values.

        `urllib.parse.parse_qs` returns a value of `['']` for parameters that are present but without value.
        """
        return not value or value == [""]
