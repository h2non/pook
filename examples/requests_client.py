import pook
import requests


# Enable mock engine
pook.on()

pook.get('httpbin.org/ip',
         reply=403, response_type='json',
         response_headers={'server': 'pook'},
         response_json={'error': 'not found'})

pook.get('httpbin.org/headers',
         reply=404, response_type='json',
         response_headers={'server': 'pook'},
         response_json={'error': 'not found'})

res = requests.get('http://httpbin.org/ip')
print('Status:', res.status_code)
print('Headers:', res.headers)
print('Body:', res.json())

res = requests.get('http://httpbin.org/headers')
print('Status:', res.status_code)
print('Headers:', res.headers)
print('Body:', res.json())

print('Is done:', pook.isdone())
print('Pending mocks:', pook.pending_mocks())
print('Unmatched requests:', pook.unmatched_requests())
