import sys, os
sys.path.append(os.path.dirname(__name__))

import requests
import pook
# from requests.exceptions import ConnectionError, HTTPError


if __name__ == '__main__':
    # m = pook.get('http://httpbin.org/ip?foo=bar', reply=204)
    # m.reply(404).type('application/json').json({'error': 'not found'})

    m = pook.get('http://httpbin.org/ip?foo=bar',
                 reply=404, response_type='json',
                 response_json={'error': 'not found'})
    # m.reply(404).type('application/json').json({'error': 'not found'})

    # Testing
    pook.activate()

    res = requests.get('http://httpbin.org/ip?foo=bar&baz=foo')
    print('Status:', res.status_code)
    print('Headers:', res.headers)
    print('Body:', res.text)

    # res = requests.get('http://httpbin.org/ip?foo=bar')
    print('Mock:', m)
    pook.disable()
    # res = requests.get('http://httpbin.org/ip')
    # print('Status:', res.status_code)
    # print('Headers:', res.headers)
    # print('Body:', res.text)
