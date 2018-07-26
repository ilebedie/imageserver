from aiohttp import web

from storage import get_storage


class StorageHandler():
    def __init__(self,  loop, executor):
        self.loop = loop
        self.executor = executor
        self.storage = get_storage()


    async def upload_jpeg(request):
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

        stored, filename_out = await self.storage.put(buf)

        if not stored:
            return web.Response(
                text=f'{filename} was previously stored as {filename_out}'
            )

        return web.Response(
            text=f'{filename} sized of {size} successfully stored as {filename_out}'
        )
