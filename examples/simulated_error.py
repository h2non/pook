import pook
import requests

# Simulated error exception
error = Exception('simulated error')

with pook.use():
    # Define mock to intercept
    pook.get('httpbin.org/status/500', error=error)

    try:
        requests.get('http://httpbin.org/status/500')
    except Exception as err:
        print('Error:', err)
