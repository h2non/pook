from websocket import WebSocket
import pook


@pook.on
def test_websocket():
    (pook.get('ws://some-non-existing.org')
        .reply(204)
        .body('test'))

    socket = WebSocket()
    socket.connect('ws://some-non-existing.org/', header=['x-custom: header'])
    socket.send('test')
