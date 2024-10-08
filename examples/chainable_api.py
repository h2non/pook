import json

import requests

import pook

# Enable mock engine
pook.on()

(
    pook.post("httpbin.org/post")
    .json({"foo": "bar"})
    .type("json")
    .header("Client", "requests")
    .reply(204)
    .headers({"server": "pook"})
    .json({"error": "simulated"})
)

res = requests.post(
    "http://httpbin.org/post",
    data=json.dumps({"foo": "bar"}),
    headers={"Client": "requests", "Content-Type": "application/json"},
)

print("Status:", res.status_code)
print("Body:", res.json())

print("Is done:", pook.isdone())
print("Pending mocks:", pook.pending_mocks())
