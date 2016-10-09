import sys, os
sys.path.append(os.path.dirname(__name__))

import requests
import pock
# from requests.exceptions import ConnectionError, HTTPError


if __name__ == '__main__':
    m = pock.get('http://httpbin.org/ip?foo=bar')
    # m.type('application/json')
    m.reply(404).json({'error': 'not found'})

    # Testing
    pock.activate()

    res = requests.get('http://httpbin.org/ip?foo=bar')
    print('Status:', res.status_code)
    print('Headers:', res.headers)
    print('Body:', res.text)

    # res = requests.get('http://httpbin.org/ip?foo=bar')
    pock.disable()
    # res = requests.get('http://httpbin.org/ip')
    # print('Status:', res.status_code)
    # print('Headers:', res.headers)
    # print('Body:', res.text)
