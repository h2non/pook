import json

from jsonschema import validate

from .base import BaseMatcher


class JSONSchemaMatcher(BaseMatcher):
    """
    JSONSchema matcher validates a request body against a given JSONSchema
    definition schema.
    """

    def __init__(self, schema):
        BaseMatcher.__init__(self, schema)

        if isinstance(schema, str):
            self.expectation = json.loads(schema)

    @BaseMatcher.matcher
    def match(self, req):
        req_json = req.json

        if not req_json:
            return False

        try:
            validate(req_json, self.expectation)
        except Exception:
            return False

        return True
