import json

import xmltodict

from ..assertion import equal
from .base import BaseMatcher


class XMLMatcher(BaseMatcher):
    """
    Match XML documents of equivalent structural value.

    XML documents are matched on the structured data in the document,
    rather than on the strict organisation of the document.

    The following two XML snippets are treated as identical by this matcher:

        <a value="one"></a>
        <b>two</b>

    ... is considered idential to ...

        <b>two</b>
        <a value="one"></a>

    In other words, the order does not matter in comparison.

    Use ``BodyMatcher`` to strictly match the exact textual structure.
    """

    def __init__(self, data):
        BaseMatcher.__init__(self, data)

        if isinstance(data, str):
            self.expectation = xmltodict.parse(data)

    def compare(self, data):
        x = json.dumps(xmltodict.parse(data), sort_keys=True)
        y = json.dumps(self.expectation, sort_keys=True)

        return equal(x, y)

    @BaseMatcher.matcher
    def match(self, req):
        xml = req.xml

        if not isinstance(xml, str):
            return False

        return self.compare(xml)
