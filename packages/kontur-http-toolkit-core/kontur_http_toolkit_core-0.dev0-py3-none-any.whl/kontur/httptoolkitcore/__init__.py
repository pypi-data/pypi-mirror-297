import logging

from kontur.httptoolkitcore.errors import ServiceError, suppress_http_error
from kontur.httptoolkitcore.header import AuthSidHeader, BasicAuthHeader, BearerAuthHeader, Header
from kontur.httptoolkitcore.service import AsyncService, Service
from kontur.httptoolkitcore.httpx_service import HttpxService, AsyncHttpxService
from kontur.httptoolkitcore.http_method import HttpMethod

__all__ = [
    "Service",
    "AsyncService",
    "HttpxService",
    "AsyncHttpxService",
    "ServiceError",
    "suppress_http_error",
    "Header",
    "AuthSidHeader",
    "BasicAuthHeader",
    "BearerAuthHeader",
    "HttpMethod",
]

logger = logging.getLogger("kontur.httptoolkitcore")
logger.addHandler(logging.NullHandler())
logger.setLevel(logging.INFO)
httpx_log = logging.getLogger("httpx")
httpx_log.propagate = False
