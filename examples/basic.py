import sys, os
sys.path.append(os.path.dirname(__name__))

import requests
import pook


with pook.use():
    def on_match(request, mock):
        print('On match:', request, mock)

    pook.get('http://httpbin.org/ip',
             reply=403, response_type='json',
             response_headers={'pepe': 'lopez'},
             response_json={'error': 'not found'},
             # callback=on_match
             )

    res = requests.get('http://httpbin.org/ip')
    print('Status:', res.status_code)
    print('Headers:', res.headers)
    print('Body:', res.json())

    # res = requests.get('http://httpbin.org/headers')
    # print('Status:', res.status_code)
    # print('Headers:', res.headers)
    # print('Body:', res.text)

    print('Is done:', pook.isdone())
    print('Pending mocks:', pook.pending_mocks())
    print('Unmatched requests:', pook.unmatched_requests())

# pook.get('http://httpbin.org/ip?foo=bar',
#          reply=404, response_type='json',
#          response_json={'error': 'not found'})
#
# # Testing
# pook.activate()
#
# res = requests.get('http://httpbin.org/ip?foo=bar')
# print('Status:', res.status_code)
# print('Headers:', res.headers)
# print('Body:', res.text)
#
# pook.disable()
