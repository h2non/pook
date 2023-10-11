import pook
import requests

# Enable mock engine
pook.on()

(
    pook.get("httpbin.org/post")
    .params({"foo": "bar"})
    .reply(204)
    .json({"error": "simulated"})
)

res = requests.get("http://httpbin.org/get", params={"foo": "bar"})
print("Status:", res.status_code)
print("Body:", res.json())

print("Is done:", pook.isdone())
print("Pending mocks:", pook.pending_mocks())
