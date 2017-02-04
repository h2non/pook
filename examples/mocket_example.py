# Be sure you have `mocket` installed:
# $ pip install mocket

import pook
import requests
from mocket.plugins.pook_mock_engine import MocketEngine

# Use mocket library as underlying mock engine
pook.set_mock_engine(MocketEngine)

# Explicitly enable pook HTTP mocking (optional)
pook.on()

# Target server URL to mock out
url = 'http://twitter.com/api/1/foobar'

# Define your mock
mock = pook.get(url,
                reply=404, times=2,
                headers={'content-type': 'application/json'},
                response_json={'error': 'foo'})

# Run first HTTP request
requests.get(url)
assert mock.calls == 1

# Run second HTTP request
res = requests.get(url)
assert mock.calls == 2

# Assert response data
assert res.status_code == 404
assert res.json() == {'error': 'foo'}

# Explicitly disable pook (optional)
pook.off()
