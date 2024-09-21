from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Tuple, Iterator

from kontur.httptoolkitcore.request import Request
from kontur.httptoolkitcore.response import Response, StreamResponse
from kontur.httptoolkitcore.sent_request import SentRequest


class BaseTransport(ABC):
    @abstractmethod
    def send(self, request: Request) -> Tuple[SentRequest, Response]:  # pragma: no cover
        pass

    @abstractmethod
    @contextmanager
    def stream(self, request: Request) -> Iterator[Tuple[SentRequest, StreamResponse]]:  # pragma: no cover
        pass
