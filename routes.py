from aiohttp import web
import handlers


def setup_routes(app):
    app.add_routes([
        web.get('/', handlers.PingHandler.handle),
        web.get('/ping', handlers.PingHandler.handle),
        web.post(
            '/upload-jpeg',
            app['handlers']['storage'].upload_jpeg
        ),
        web.post(
            '/fetch-jpeg',
            app['handlers']['storage'].fetch_jpeg
        ),
    ])
