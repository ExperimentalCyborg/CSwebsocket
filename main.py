import mimetypes
import os

import socketio
from aiohttp import web

from clock import Clock
from datasource import Data

sio = socketio.AsyncServer(ping_interval=30)
app = web.Application()
datasource = None
poll_rate = 0.1  # Lower is quicker client updates, higher is less server load.
web_folder = 'web'


@sio.event
async def connect(sid, environ):
    await sio.save_session(sid, {
        'authenticated': False,
        'token': None
    })
    print(f"{sid} connected")


@sio.event
async def authenticate(sid, token):
    session_valid = float(token) > 0.1  # Simulate comparing token and client IP to a database of valid sessions
    if session_valid:
        await sio.save_session(sid, {
            'authenticated': True,
            'token': token
        })
        print(f'{sid} authenticated with token "{token}"')
        await sio.emit('authenticated')
    else:
        await sio.emit('invalidated')


@sio.event
async def subscribe(sid, topic):
    session = await sio.get_session(sid)
    if not session['authenticated']:
        return False

    print(f"{sid} subscribed to {topic}")
    current_value = datasource[topic]
    await sio.emit(topic, current_value, room=sid)
    while len(sio.rooms(sid)):
        value = datasource.wait_for_update(poll_rate, topic, current_value)
        if value != current_value:
            await sio.emit(topic, value, room=sid)
            current_value = value
            print(f'sent {topic} update to {sid}')


@sio.event
async def disconnect(sid):
    await sio.save_session(sid, None)
    print(f"{sid} disconnected")


async def serve_file(request):
    path = request.path[1:].replace('..', '?')
    if len(path) < 1:
        path = 'index.html'

    path = os.path.join(web_folder, path)

    if os.path.isfile(path):
        try:
            with open(path) as f:
                return web.Response(text=f.read(), content_type=mimetypes.guess_type(path)[0])
        except Exception as err:
            print(err)
    else:
        return web.Response(text='404', content_type='text/html', status=404)


async def serve_index(request):
    return await serve_file(request)


if __name__ == '__main__':
    datasource = Data()
    clock = Clock(datasource, 'counter1', 2)
    clock.start()

    sio.attach(app)
    app.router.add_get('/', serve_index)
    app.router.add_get(r'/{fname}', serve_file)
    web.run_app(app)
