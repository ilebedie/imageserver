import aiohttp
from aiohttp import web
import logging

from storage import get_storage
from image_processing import make_thumbnail


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
        logging.info(f'Uploaded {size} bytes')

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
        url = request.query.get('url')
        #logging.info(request.query)
        if not url:
            return web.Response(status=400, text='Url is missing')

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                size = 0
                buf = b''
                chunk = await resp.content.read(8192)
                while chunk:
                    buf += chunk
                    size += len(chunk)
                    chunk = await resp.content.read(8192)
                logging.info(f'Uploaded {size} bytes')

                stored, file_url = await self.storage.put(buf)
                resp_json = {
                    'stored': stored,
                    'orig_file': file_url,
                }
                return web.json_response(resp_json)
