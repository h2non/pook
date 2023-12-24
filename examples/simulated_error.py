import pook
import requests


# Enable mock engine
pook.on()

# Simulated error exception on request matching
pook.get("httpbin.org/status/500", error=Exception("simulated error"))

try:
    requests.get("http://httpbin.org/status/500")
except Exception as err:
    print("Error:", err)
