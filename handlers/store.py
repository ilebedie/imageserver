from aiohttp import web


class StorageHandler():
    def __init__(self,  loop, executor):
        self.loop = loop
        self.executor = executor


    async def upload(request):
        #try:
            #mime, body = await self.loop.run_in_executor(
            #    self.executor,
            #    generate_thumbnail
            #)
            #s3.put
        return web.Response(text='PONG')
