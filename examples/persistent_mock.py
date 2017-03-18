import pook
import requests


# Enable mock engine
pook.on()

(pook.get('httpbin.org')
    .headers({'Client': 'requests'})
    .persist()
    .reply(400)
    .headers({'server': 'pook'})
    .json({'error': 'simulated'}))

res = requests.get('http://httpbin.org',
                   headers={'Client': 'requests'})

print('Status:', res.status_code)
print('Headers:', res.headers)
print('Body:', res.json())

print('Is done:', pook.isdone())
print('Pending mocks:', pook.pending_mocks())
