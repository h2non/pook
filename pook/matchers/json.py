import json
from .base import BaseMatcher


class JSONMatcher(BaseMatcher):
    """
    JSONMatcher implements a JSON body matcher supporting strict structure
    and regular expression based comparisons.
    """

    def __init__(self, data):
        BaseMatcher.__init__(self, data)

        if isinstance(data, str):
            self.expectation = json.loads(data)

    @BaseMatcher.matcher
    def match(self, req):
        body = req.body

        if isinstance(body, str):
            try:
                body = json.loads(body)
            except:
                return False

        x = json.dumps(self.expectation, sort_keys=True, indent=4)
        y = json.dumps(body, sort_keys=True, indent=4)

        return self.compare(x, y)
