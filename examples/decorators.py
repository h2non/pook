import requests

import pook


@pook.get("http://httpbin.org/status/500", reply=204)
@pook.get("http://httpbin.org/status/400", reply=200, persist=True)
def fetch(url):
    return requests.get(url)


# Test function
res = fetch("http://httpbin.org/status/400")
print("#1 status:", res.status_code)

res = fetch("http://httpbin.org/status/500")
print("#2 status:", res.status_code)

print("Is done:", pook.isdone())
print("Pending mocks:", pook.pending_mocks())

# Disable mock engine
pook.off()

# Test real request
res = requests.get("http://httpbin.org/status/400")
print("Test status:", res.status_code)
