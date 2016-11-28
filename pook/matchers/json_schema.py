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
        body = req.body

        if isinstance(body, str):
            try:
                body = json.loads(body)
            except:
                return False

        if not body:
            return False

        try:
            validate(body, self.expectation)
        except:
            return False

        return True
