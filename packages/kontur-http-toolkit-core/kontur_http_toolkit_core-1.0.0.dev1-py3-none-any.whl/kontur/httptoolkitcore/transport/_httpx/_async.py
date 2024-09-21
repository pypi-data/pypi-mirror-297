from contextlib import asynccontextmanager
from typing import AsyncIterator, Tuple

from kontur.httptoolkitcore.request import Request
from kontur.httptoolkitcore.response import Response, AsyncStreamResponse
from kontur.httptoolkitcore.transport._httpx._session._async import AsyncHttpxSession

from kontur.httptoolkitcore.sent_request import SentRequest
from ._base import BaseHttpxTransport
from kontur.httptoolkitcore.transport import BaseAsyncTransport


class AsyncHttpxTransport(BaseAsyncTransport, BaseHttpxTransport):
    _session_class = AsyncHttpxSession

    async def send(self, request: Request) -> Tuple[SentRequest, Response]:
        httpx_request = self._build_httpx_request(request)
        sent_request = self._prepare_sent_request(request, httpx_request)
        with self._managed_session(sent_request) as async_session:
            return sent_request, Response(await async_session.send(httpx_request))

    @asynccontextmanager
    async def stream(self, request: Request) -> AsyncIterator[Tuple[SentRequest, AsyncStreamResponse]]:
        httpx_request = self._build_httpx_request(request)
        sent_request = self._prepare_sent_request(request, httpx_request)
        with self._managed_session(sent_request) as async_session:
            async with async_session.stream(httpx_request) as response:
                yield sent_request, AsyncStreamResponse(response)
