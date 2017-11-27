import pook
import requests


# Enable mock engine
pook.on()

# Declare mock
(pook.get('httpbin.org')
    .times(2)
    .reply(400)
    .headers({'server': 'pook'})
    .json({'error': 'simulated'}))

# Mock request 1
res = requests.get('http://httpbin.org')
print('#1 status:', res.status_code)
print('#1 body:', res.json())

# Mock request 2
res = requests.get('http://httpbin.org')
print('#2 status:', res.status_code)
print('#2 body:', res.json())

# Real request 3
try:
    requests.get('http://httpbin.org')
except Exception as err:
    print('Request #3 not matched due to expired mock')

print('Is done:', pook.isdone())
print('Pending mocks:', pook.pending_mocks())
