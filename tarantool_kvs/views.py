from aiohttp.web import View

from tarantool_kvs.schemas import *
from tarantool_kvs.utils import json_response
from tarantool_kvs.validation import validate_request_data
from tarantool.error import DatabaseError
from tarantool_kvs.exceptions import AlreadyExistError, NotFoundError


class KVPostView(View):
    @validate_request_data(body_schema=FILTERS_SCHEMA_POST)
    async def post(self):
        data = await self.request.json()
        engine = self.request.app["engine"]
        try:
            # В документации написано, что значение может быть str, но на str ругается
            # Поэтому такое дурацкое решение с hash
            key = hash(data["key"])
            engine.insert((key, data["value"]))
        except DatabaseError:
            raise AlreadyExistError(f"key {data['key']} already exist")

        return json_response(data, status=200)


class KVOtherView(View):
    async def get(self):
        engine = self.request.app["engine"]
        # В документации написано, что значение может быть str, но на str ругается
        key = hash(self.request.match_info["id"])
        dict_response = engine.select(key)
        if not dict_response:
            raise NotFoundError(f"key {self.request.match_info['id']} not found")
        dict_response[0][0] = self.request.match_info["id"]
        return json_response(dict_response, status=200)

    @validate_request_data(body_schema=FILTERS_SCHEMA_PUT)
    async def put(self):
        data_id = hash(self.request.match_info["id"])
        data = await self.request.json()
        engine = self.request.app["engine"]
        dict_response = engine.update(data_id, [('=', 1, data["value"])])
        if not dict_response:
            raise NotFoundError(f"key {self.request.match_info['id']} not found")
        return json_response(dict_response, status=200)

    async def delete(self):
        # В документации написано, что значение может быть str, но на str ругается
        data_id = hash(self.request.match_info["id"])
        engine = self.request.app["engine"]
        dict_response = engine.delete(data_id)
        if not dict_response:
            raise NotFoundError(f"key {self.request.match_info['id']} not found")
        return json_response(dict_response, status=200)
