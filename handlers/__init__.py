from aiohttp import web


class PingHandler():
    async def handle(request):
        return web.Response(text='PONG')

