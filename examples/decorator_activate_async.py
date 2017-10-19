import pook
import asyncio
import aiohttp

#
# NOTE: requires Python 3.5+
#

@pook.on
async def run():
    pook.get('httpbin.org/ip', reply=403,
             response_headers={'pepe': 'lopez'},
             response_json={'error': 'not found'})

    async with aiohttp.ClientSession(loop=loop) as session:
        async with session.get('http://httpbin.org/ip') as res:
            print('Status:', res.status)
            print('Headers:', res.headers)
            print('Body:', await res.text())

            print('Is done:', pook.isdone())
            print('Pending mocks:', pook.pending_mocks())
            print('Unmatched requests:', pook.unmatched_requests())


loop = asyncio.get_event_loop()
loop.run_until_complete(run())
