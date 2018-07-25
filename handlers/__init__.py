from aiohttp import web

from .store import StorageHandler

def setup_handlers(app, loop, executor):
    ping_handler = PingHandler()
    storage_handler = StorageHandler(loop, executor)

    app['handlers'] = [
        ping_handler,
        storage_handler,
    ]


class PingHandler():
    async def handle(request):
        return web.Response(text='PONG')

