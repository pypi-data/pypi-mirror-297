from abc import abstractmethod, ABC
from contextlib import asynccontextmanager
from typing import Tuple, AsyncIterator

from kontur.httptoolkitcore.request import Request
from kontur.httptoolkitcore.response import Response, AsyncStreamResponse
from kontur.httptoolkitcore.sent_request import SentRequest


class BaseAsyncTransport(ABC):
    @abstractmethod
    async def send(self, request: Request) -> Tuple[SentRequest, Response]:  # pragma: no cover
        pass

    @asynccontextmanager
    @abstractmethod
    def stream(self, request: Request) -> AsyncIterator[Tuple[SentRequest, AsyncStreamResponse]]:  # pragma: no cover
        pass
