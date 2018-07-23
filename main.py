from aiohttp import web
from routes import setup_routes
from settings import config

if __name__ == '__main__':
    app = web.Application()
    app['config'] = config
    setup_routes(app)
    web.run_app(app)
