import asyncio
import argparse
import logging

from aiohttp import web
import concurrent.futures

from .routes import setup_routes
from .handlers import setup_handlers
from .settings import config


logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)
logger.propagate = False


def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('--host', default='127.0.0.1', type=str)
        parser.add_argument('--port', default=8000, type=int)
        host, port = parser.parse_args()

        config['HOST'] = config.get('HOST') or host
        config['PORT'] = config.get('PORT') or port

        middlewares = []
        app = web.Application(middlewares=middlewares)

        executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=config['NUM_CORES']
        )
        loop = asyncio.get_event_loop()

        app['config'] = config
        setup_handlers(app, loop, executor)
        setup_routes(app)
        web.run_app(app)
    finally:
        logger.info('Exiting app')


if __name__ == '__main__':
    main()
