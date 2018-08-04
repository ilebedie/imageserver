from .filesystem import FileSystemStorage
from settings import config

__all__ = ['get_storage', 'setup_storage']

__storage = None


def setup_storage(loop, executor):
    global __storage
    if config['DEBUG'] and not __storage:
        __storage = FileSystemStorage(loop, executor)
    elif __storage:
        raise RuntimeError('Storage has already been setup')
    else:
        raise NotImplementedError


def get_storage():
    global __storage
    if not __storage:
        raise RuntimeError('NotInitialized')

    return __storage
