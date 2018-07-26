import aiofiles

from os import listdir
from os.path import isfile, join

from ..settings import config
from ..utils.hash import get_hash


class FileSystemStorage:
    asset_path = config['FS_STORAGE_PATH']

    def __init__(self, loop, executor):
        self.loop = loop
        self.executor = executor
        self.files = self.get_list_of_existing_files()

    async def put(self, buf, mime='jpeg'):
        hash = await self.loop.run_in_executor(
            self.executor,
            get_hash,
            buf
        )
        filename = f`{str(hash)}.{mime}`
        fpath = join(asset_path, filename)
        if fpath in self.files:
            return

        async with aiofiles.open(fpath, 'w') as f:
            await f.write(buf)

        self.files.add(files)

    @classmethod
    def get_list_of_existing_files(cls):
        return {
            f for f in listdir(cls.asset_path)
            if isfile(join(cls.asset_path, f))
        }
