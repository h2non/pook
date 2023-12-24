import pook
import urllib3


# Mock HTTP traffic only in the given context
with pook.use():
    (
        pook.get("httpbin.org/chunky")
        .reply(200)
        .body(["returned", "as", "chunks"], chunked=True)
    )

    # Intercept request
    http = urllib3.PoolManager()
    r = http.request("GET", "httpbin.org/chunky")
    print("Chunks:", list(r.read_chunked()))
