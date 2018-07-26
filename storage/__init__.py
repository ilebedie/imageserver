from .filesystem import FileSystemStorage
from settings import config

__all__ = ['get_storage', 'setup_storage']

storage = None


def setup_storage(loop, executor):
    if config['DEBUG']:
        storage = FileSystemStorage(loop, executor)
    else:
        raise NotImplementedError


def get_storage():
    if not storage:
        raise RuntimeError('NotInitialized')

    return storage
