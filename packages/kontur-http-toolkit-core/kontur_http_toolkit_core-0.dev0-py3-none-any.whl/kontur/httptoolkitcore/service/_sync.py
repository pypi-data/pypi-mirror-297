from contextlib import contextmanager
from typing import Iterator, List, Optional, Tuple, Union, Dict, BinaryIO

from kontur.httptoolkitcore.errors import HttpError, TransportError, ServiceError
from kontur.httptoolkitcore.header import Header
from kontur.httptoolkitcore.request import Request
from kontur.httptoolkitcore.response import BaseResponse, Response, StreamResponse

from kontur.httptoolkitcore.sent_request import SentRequest
from kontur.httptoolkitcore.http_method import HttpMethod
from kontur.httptoolkitcore.transport import BaseTransport


class Service:
    def __init__(
        self,
        transport: BaseTransport,
        headers: Tuple[Header, ...] = (),
    ) -> None:
        self._transport = transport
        self._headers: Tuple[Header, ...] = headers

    @property
    def headers(self) -> Tuple[Header, ...]:
        return self._headers

    def request(self, request: Request) -> Response:
        with self._managed_transport() as transport:
            sent_request, response = transport.send(request)
            self._validate_response(sent_request, response)
            return response

    def post(
        self,
        path: str,
        headers: Tuple[Header, ...] = (),
        params: Optional[dict] = None,
        body: Optional[str] = None,
        json: Optional[Union[dict, List]] = None,
        files: Optional[Dict[str, Union[BinaryIO, Tuple[str, BinaryIO, str]]]] = None,
    ) -> Response:
        request = Request(
            method=HttpMethod.POST,
            path=path,
            headers=self.headers + headers,
            params=params,
            body=body,
            json=json,
            files=files,
        )
        return self.request(request)

    def patch(
        self,
        path: str,
        headers: Tuple[Header, ...] = (),
        params: Optional[dict] = None,
        body: Optional[str] = None,
        json: Optional[Union[dict, List]] = None,
        files: Optional[Dict[str, Union[BinaryIO, Tuple[str, BinaryIO, str]]]] = None,
    ) -> Response:
        request = Request(
            method=HttpMethod.PATCH,
            path=path,
            headers=self.headers + headers,
            params=params,
            body=body,
            json=json,
            files=files,
        )
        return self.request(request)

    def put(
        self,
        path: str,
        headers: Tuple[Header, ...] = (),
        params: Optional[dict] = None,
        body: Optional[str] = None,
        json: Optional[Union[dict, List]] = None,
        files: Optional[Dict[str, Union[BinaryIO, Tuple[str, BinaryIO, str]]]] = None,
    ) -> Response:
        request = Request(
            method=HttpMethod.PUT,
            path=path,
            headers=self.headers + headers,
            params=params,
            body=body,
            json=json,
            files=files,
        )
        return self.request(request)

    def delete(
        self,
        path: str,
        headers: Tuple[Header, ...] = (),
        params: Optional[dict] = None,
        body: Optional[str] = None,
        json: Optional[Union[dict, List]] = None,
        files: Optional[Dict[str, Union[BinaryIO, Tuple[str, BinaryIO, str]]]] = None,
    ) -> Response:
        request = Request(
            method=HttpMethod.DELETE,
            path=path,
            headers=self.headers + headers,
            params=params,
            body=body,
            json=json,
            files=files,
        )
        return self.request(request)

    def get(
        self,
        path: str,
        headers: Tuple[Header, ...] = (),
        params: Optional[dict] = None,
    ) -> Response:
        request = Request(
            method=HttpMethod.GET,
            path=path,
            headers=self.headers + headers,
            params=params,
            body=None,
            json=None,
            files=None,
        )
        return self.request(request)

    @staticmethod
    def _validate_response(sent_request: SentRequest, response: BaseResponse) -> None:
        if not response.ok:
            if isinstance(response, StreamResponse):
                response.read()
            raise HttpError(sent_request, response)

    @contextmanager
    def stream_request(
        self,
        request: Request,
    ) -> Iterator[StreamResponse]:
        with self._managed_transport() as transport:
            with transport.stream(request) as (sent_request, stream_response):
                self._validate_response(sent_request, stream_response)
                yield stream_response

    @contextmanager
    def post_stream(
        self,
        path: str,
        headers: Tuple[Header, ...] = (),
        params: Optional[dict] = None,
        body: Optional[str] = None,
        json: Optional[Union[dict, List]] = None,
        files: Optional[Dict[str, Union[BinaryIO, Tuple[str, BinaryIO, str]]]] = None,
    ) -> Iterator[StreamResponse]:
        request = Request(
            method=HttpMethod.POST,
            path=path,
            headers=self.headers + headers,
            params=params,
            body=body,
            json=json,
            files=files,
        )
        with self.stream_request(request) as stream_response:
            yield stream_response

    @contextmanager
    def patch_stream(
        self,
        path: str,
        headers: Tuple[Header, ...] = (),
        params: Optional[dict] = None,
        body: Optional[str] = None,
        json: Optional[Union[dict, List]] = None,
        files: Optional[Dict[str, Union[BinaryIO, Tuple[str, BinaryIO, str]]]] = None,
    ) -> Iterator[StreamResponse]:
        request = Request(
            method=HttpMethod.PATCH,
            path=path,
            headers=self.headers + headers,
            params=params,
            body=body,
            json=json,
            files=files,
        )
        with self.stream_request(request) as stream_response:
            yield stream_response

    @contextmanager
    def put_stream(
        self,
        path: str,
        headers: Tuple[Header, ...] = (),
        params: Optional[dict] = None,
        body: Optional[str] = None,
        json: Optional[Union[dict, List]] = None,
        files: Optional[Dict[str, Union[BinaryIO, Tuple[str, BinaryIO, str]]]] = None,
    ) -> Iterator[StreamResponse]:
        request = Request(
            method=HttpMethod.PUT,
            path=path,
            headers=self.headers + headers,
            params=params,
            body=body,
            json=json,
            files=files,
        )
        with self.stream_request(request) as stream_response:
            yield stream_response

    @contextmanager
    def delete_stream(
        self,
        path: str,
        headers: Tuple[Header, ...] = (),
        params: Optional[dict] = None,
        body: Optional[str] = None,
        json: Optional[Union[dict, List]] = None,
        files: Optional[Dict[str, Union[BinaryIO, Tuple[str, BinaryIO, str]]]] = None,
    ) -> Iterator[StreamResponse]:
        request = Request(
            method=HttpMethod.DELETE,
            path=path,
            headers=self.headers + headers,
            params=params,
            body=body,
            json=json,
            files=files,
        )
        with self.stream_request(request) as stream_response:
            yield stream_response

    @contextmanager
    def get_stream(
        self,
        path: str,
        headers: Tuple[Header, ...] = (),
        params: Optional[dict] = None,
    ) -> Iterator[StreamResponse]:
        request = Request(
            method=HttpMethod.GET,
            path=path,
            headers=self.headers + headers,
            params=params,
            body=None,
            json=None,
            files=None,
        )
        with self.stream_request(request) as stream_response:
            yield stream_response

    @contextmanager
    def _managed_transport(self) -> Iterator[BaseTransport]:
        try:
            yield self._transport

        except TransportError as exc:
            raise ServiceError(exc.request) from exc
