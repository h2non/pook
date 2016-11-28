import json
import pook
import requests


(pook.post('httpbin.org/post')
    .json({'foo': 'bar'})
    .type('json')
    .header({'Client': 'requests'})
    .reply(204)
    .headers({'server': 'pook'})
    .json({'error': 'simulated'}))

res = requests.post('http://httpbin.org/post',
                    headers={'Client': 'requests'},
                    data=json.dumps({'foo': 'bar'}))

print('Status:', res.status_code)
print('Body:', res.json())

print('Is done:', pook.isdone())
print('Pending mocks:', pook.pending_mocks())
