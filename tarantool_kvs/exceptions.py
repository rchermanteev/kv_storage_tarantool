from typing import Any, Dict, Optional

from aiohttp.web import HTTPClientError


class BaseClientError(HTTPClientError):
    status_code = 400

    def __init__(
        self, error_msg: str, *, fields_errors: Optional[Dict] = None, extra: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(reason=error_msg)
        self.fields_errors = fields_errors
        self.extra = extra


class JsonDecodingError(BaseClientError):
    status_code = 400


class ValidationError(BaseClientError):
    status_code = 400


class NotFoundError(BaseClientError):
    status_code = 404


class AlreadyExistError(BaseClientError):
    status_code = 409


class CommchannelUpdateError(BaseClientError):
    status_code = 400
