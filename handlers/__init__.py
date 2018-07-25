from aiohttp import web

from .store import StorageHandler

def setup_handlers(app, loop, executor):


class PingHandler():
    async def handle(request):
        return web.Response(text='PONG')

