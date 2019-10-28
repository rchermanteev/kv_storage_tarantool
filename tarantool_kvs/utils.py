import logging
from functools import partial
from typing import Any, Dict, Optional


import ujson
from aiohttp.web import HTTPClientError, Response
from aiohttp.web import json_response as _json_response
from aiohttp.web import middleware

from tarantool_kvs.exceptions import BaseClientError, JsonDecodingError


json_response = partial(_json_response, dumps=ujson.dumps)


def error_response(
    error_msg: str, fields_errors: Optional[Dict] = None, extra: Optional[Dict[str, Any]] = None, status: int = 400
) -> Response:
    """ Функция для формирования сообщения об ошибке.
    Error data:
        Опциональное поле для подробростей ошибки.
        Например, подробное описание ошибки валидации.
    """

    data: Dict[str, Any] = {"error": error_msg}

    if fields_errors:
        data["fields"] = fields_errors

    if extra:
        data.update(extra)

    return json_response(data=data, status=status)


@middleware
async def catch_exceptions(request, handler):
    """ Отправить error_response на любое неперехваченное исключение в обработчике запроса. """
    try:
        resp = await handler(request)

    except BaseClientError as client_error:
        logging.debug("Client Error: %s", client_error)
        return error_response(
            error_msg=str(client_error),
            fields_errors=client_error.fields_errors,
            extra=client_error.extra,
            status=client_error.status_code,
        )

    except HTTPClientError as exc:
        logging.debug("Client Error -- %s: %s", type(exc), exc)
        return error_response(str(exc), status=exc.status_code)

    except Exception as exc:
        logging.error(str(exc), exc_info=True)
        return error_response("internal error", status=500)

    return resp
