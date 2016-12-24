import pook
import requests


# Registry mock definition
(pook.get('httpbin.org')
    .path(pook.regex('/foo/[a-z]+/baz'))
    .header('Client', pook.regex('requests|pook'))
    .times(2)
    .reply(200)
    .headers({'server': 'pook'})
    .json({'foo': 'bar'}))

# Perform request
res = requests.get('http://httpbin.org/foo/bar/baz',
                   headers={'Client': 'requests'})
print('Status:', res.status_code)
print('Body:', res.json())

# Perform second request
res = requests.get('http://httpbin.org/foo/foo/baz',
                   headers={'Client': 'pook'})
print('Status:', res.status_code)
print('Body:', res.json())

print('Is done:', pook.isdone())
print('Pending mocks:', pook.pending_mocks())
