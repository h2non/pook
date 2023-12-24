import json
import pook
import requests


schema = {
    "type": "object",
    "properties": {
        "foo": {"type": "string"},
    },
}

# Enable mock engine
pook.on()

(
    pook.post("httpbin.org/post")
    .jsonschema(schema)
    .reply(204)
    .json({"error": "simulated"})
)

res = requests.post("http://httpbin.org/post", data=json.dumps({"foo": "bar"}))

print("Status:", res.status_code)
print("Body:", res.json())

print("Is done:", pook.isdone())
print("Pending mocks:", pook.pending_mocks())
