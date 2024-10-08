import json

from ..assertion import equal
from .base import BaseMatcher


class JSONMatcher(BaseMatcher):
    """
    Match JSON documents of equivalent value.

    JSON documents are matched on the structured data in the document,
    rather than on the strict organisation of the document.

    The following two JSON snippets are treated as identical by this matcher:

        {"a": "one", "b": ["two"]}

    ... is considered idential to ...

        {"b": ["two"], "a": "one"}

    In other words, the order does not matter in comparison.

    Use ``BodyMatcher`` to strictly match the exact textual structure.
    """

    def __init__(self, data):
        BaseMatcher.__init__(self, data)

        if isinstance(data, str):
            self.expectation = json.loads(data)

    @BaseMatcher.matcher
    def match(self, req):
        x = json.dumps(self.expectation, sort_keys=True, indent=4)
        y = json.dumps(req.json, sort_keys=True, indent=4)

        return equal(x, y)
