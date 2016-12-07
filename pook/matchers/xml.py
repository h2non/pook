import json
import xmltodict
from .base import BaseMatcher


class XMLMatcher(BaseMatcher):
    """
    XMLMatcher implements a XML body matcher supporting both strict structure
    comparison and regular expression.
    """

    def __init__(self, data):
        BaseMatcher.__init__(self, data)

        if isinstance(data, str):
            self.expectation = xmltodict.parse(data)

    def compare(self, data):
        x = json.dumps(xmltodict.parse(data), sort_keys=True)
        y = json.dumps(self.expectation, sort_keys=True)

        return x == y

    @BaseMatcher.matcher
    def match(self, req):
        data = req.body

        if not isinstance(data, str):
            return False

        return self.compare(data)
