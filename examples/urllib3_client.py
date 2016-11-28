import pook
import urllib3


# Mock HTTP traffic only in the given context
with pook.use():
    pook.get('http://httpbin.org/status/404').reply(204)

    # Intercept request
    http = urllib3.PoolManager()
    r = http.request('GET', 'http://httpbin.org/status/404')
    print('#1 status:', r.status)


# Real request outside of the context manager
http = urllib3.PoolManager()
r = http.request('GET', 'http://httpbin.org/status/404')
print('#2 status:', r.status)
