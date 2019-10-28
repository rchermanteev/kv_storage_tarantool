import asyncio
import logging
import aiohttp_autoreload
import tarantool
from aiohttp import web


from tarantool_kvs.middleware import close_http_client, init_http_client
from tarantool_kvs.routes import inject_routes
from tarantool_kvs.utils import catch_exceptions
import config


if config.ENABLE_AUTORELOAD:
    aiohttp_autoreload.start()


async def init(loop):

    app = web.Application(loop=loop, middlewares=[catch_exceptions])
    
    # Возникли проблемы с созданием своего space
    app["engine"] = tarantool.connect("localhost", 3301).space("example")

    # fmt: off
    app.on_startup.extend([
        init_http_client,
    ])

    app.on_cleanup.extend([
        close_http_client,
    ])
    # fmt: on

    inject_routes(app)
    return app


def run():
    logging.basicConfig(level=logging.INFO)

    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init(loop))

    web.run_app(app, host=config.CR_HOST, port=config.CR_PORT)
