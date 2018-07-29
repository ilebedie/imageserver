from .filesystem import FileSystemStorage
from settings import config

__all__ = ['get_storage', 'setup_storage']

storage = None


def setup_storage(loop, executor):
    global storage
    if config['DEBUG'] and not storage:
        storage = FileSystemStorage(loop, executor)
    elif storage:
        raise RuntimeError('Storage has already been setup')
    else:
        raise NotImplementedError


def get_storage():
    global storage
    if not storage:
        raise RuntimeError('NotInitialized')

    return storage
