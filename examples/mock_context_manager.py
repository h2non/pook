import pook
import requests


# Define a new mock that will be only active within the context manager
with pook.get('httpbin.org/ip', reply=403,
              response_headers={'pepe': 'lopez'},
              response_json={'error': 'not found'}) as mock:

    res = requests.get('http://httpbin.org/ip')
    print('#1 Status:', res.status_code)
    print('#1 Headers:', res.headers)
    print('#1 Body:', res.json())
    print('----------------')

    res = requests.get('http://httpbin.org/ip')
    print('#2 Status:', res.status_code)
    print('#2 Headers:', res.headers)
    print('#2 Body:', res.json())
    print('----------------')

    print('Mock is done:', mock.isdone())
    print('Mock matches:', mock.total_matches)

    print('Is done:', pook.isdone())
    print('Pending mocks:', pook.pending_mocks())
    print('Unmatched requests:', pook.unmatched_requests())


# Explicitly disable mock engine
pook.off()

# Perform a real HTTP request since we are running the
# request outside of the context manager
res = requests.get('http://httpbin.org/ip')
print('#3 Status:', res.status_code)
print('#3 Headers:', res.headers)
print('#3 Body:', res.json())
