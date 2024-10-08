import requests

import pook

# Enable mock engine
pook.on()

(
    pook.get("httpbin.org/get")
    .params({"foo": "bar"})
    .reply(201)
    .json({"error": "simulated"})
)

res = requests.get("http://httpbin.org/get", params={"foo": "bar"})

assert res.status_code == 201
assert res.json() == {"error": "simulated"}
assert pook.isdone()
assert pook.pending_mocks() == []
