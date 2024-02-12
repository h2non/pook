import pook
import httpx


# Enable mock engine
pook.on()

# Enable network mode
pook.enable_network()

(
    pook.get("httpbin.org/headers")
    .reply(204)
    .headers({"server": "pook"})
    .json({"error": "simulated"})
)

res = httpx.get("http://httpbin.org/headers")
print("Mock status:", res.status_code)

# Real network request, since pook cannot match any mock
res = httpx.get("http://httpbin.org/ip")
print("Real status:", res.status_code)

print("Is done:", pook.isdone())
print("Pending mocks:", pook.pending_mocks())

# Disable network mode once we're done
pook.disable_network()
