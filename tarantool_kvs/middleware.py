import aiohttp


async def init_http_client(app):
    app["http_client"] = aiohttp.ClientSession()


async def close_http_client(app):
    if "http_client" in app:
        await app["http_client"].close()
