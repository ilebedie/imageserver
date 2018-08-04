import aiohttp
from aiohttp import web

from storage import get_storage
from image_processing import make_thumbnail


routes = web.RouteTableDef()

class StorageHandler():
    def __init__(self,  loop, executor):
        self.loop = loop
        self.executor = executor
        self.storage = get_storage()

    async def upload_jpeg(self, request):
        reader = await request.multipart()

        # /!\ Don't forget to validate your inputs /!\
        # check file size
        # handle big files

        field = await reader.next()
        assert field.name == 'name'
        name = await field.read(decode=True)

        field = await reader.next()
        assert field.name == 'file'
        filename = field.filename

        size = 0
        buf = b''

        chunk = await field.read_chunk()  # 8192 bytes by default.
        while chunk:
            buf += chunk
            size += len(chunk)
            chunk = await field.read_chunk()

        stored, file_url = await self.storage.put(buf)
        resp_json = {
            'stored': stored,
            'orig_file': file_url,
        }

        field = await reader.next()
        assert field.name == 'create_thumbnail'
        create_thumbnail = await field.read(decode=True)

        thubmnail_100 = None
        thubmnail_200 = None

        if create_thumbnail == b'true':
            thumbnail_100 = await self.loop.run_in_executor(
                self.executor,
                make_thumbnail,
                buf, 100
            )
            thumbnail_200 = await self.loop.run_in_executor(
                self.executor,
                make_thumbnail,
                buf, 200
            )

            _, thumbn_100_url = await self.storage.put(
                thumbnail_100
            )
            _, thumbn_200_url = await self.storage.put(
                thumbnail_200
            )
            resp_json['thumbnail_100'] = thumbn_100_url
            resp_json['thumbnail_200'] = thumbn_200_url

        return web.json_response(resp_json)

    async def fetch_jpeg(self, request):
        url = request.get('url')
        if not url:
            return Response(status=400, text='Url is missing')
        return Response(status=501, text='Url is missing')

       # async with aiohttp.ClientSession() as session:
       #     async with session.get(url) as resp:
       #         await resp.content.read(10)
       #         chunk await resp.content.read() # what is chunk_size
       #         while True:
       #             chunk = await resp.content.read() # what is chunk_size
       # with open(filename, 'wb') as fd:
       #         if not chunk:
       #             break
       #         fd.write(chunk)
       # stored, file_url = await self.storage.put(buf)
