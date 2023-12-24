import pook
import requests

# Enable mock engine
pook.on()

(
    pook.get("httpbin.org/get")
    .params({"foo": "bar"})
    .reply(204)
    .json({"error": "simulated"})
)

res = requests.get("http://httpbin.org/get", params={"foo": "bar"})

assert res.status_code == 204
assert res.json() == {"error": "simulated"}
assert pook.isdone()
assert pook.pending_mocks() == []
