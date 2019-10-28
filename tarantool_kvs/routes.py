from aiohttp import web

from tarantool_kvs.views import *


def inject_routes(app):
    # fmt: off
    app.add_routes([
        web.view('/kv', KVPostView),
        web.view('/kv/{id}', KVOtherView),
    ])
    # fmt: on
