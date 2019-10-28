import ujson
from cerberus import Validator

from tarantool_kvs.exceptions import *


def validate_request_data(body_schema: Dict = None):
    def wrap(method):
        async def wrapper(self):
            if body_schema:
                try:
                    body_data = await self.request.json(loads=ujson.loads)
                except (ValueError, TypeError):
                    raise ValidationError("Cannot decode json")

                body_validator = Validator(body_schema)

                if not body_validator.validate(body_data):
                    raise ValidationError("Validation Error", fields_errors=body_validator.errors)
            return await method(self)
        return wrapper
    return wrap
