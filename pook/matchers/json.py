import json
from .base import BaseMatcher
from ..types import isregex


class JSONMatcher(BaseMatcher):
    """
    JSONMatcher implements a JSON body matcher supporting strict structure
    and regular expression based comparisons.
    """

    def __init__(self, data):
        BaseMatcher.__init__(self, data)

        if isinstance(data, str):
            self.expectation = json.loads(data)

    def compare(self, body):
        if isinstance(body, str):
            try:
                body = json.loads(body)
            except:
                return False

        x = json.dumps(self.expectation, sort_keys=True)
        y = json.dumps(body, sort_keys=True)

        return x == y

    @BaseMatcher.matcher
    def match(self, req):
        body = req.body

        if not isinstance(body, str):
            return False

        if body == self.expectation:
            return True

        if isregex(self.expectation):
            return self.expectation.match(body or '') is not None

        return self.compare(body)
