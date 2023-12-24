import pook
import requests


with pook.api.context():
    pook.get(
        "httpbin.org/ip",
        reply=403,
        response_headers={"pepe": "lopez"},
        response_json={"error": "not found"},
    )

    res = requests.get("http://httpbin.org/ip")
    print("Status:", res.status_code)
    print("Headers:", res.headers)
    print("Body:", res.json())

    print("Is done:", pook.isdone())
    print("Pending mocks:", pook.pending_mocks())
    print("Unmatched requests:", pook.unmatched_requests())
