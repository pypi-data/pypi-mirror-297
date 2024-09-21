from typing import Any

from ._base import BaseResponse


class Response(BaseResponse):
    @property
    def content(self) -> bytes:
        return self._response.content

    @property
    def text(self) -> str:
        return self._response.text

    def json(self) -> Any:
        return self._response.json()
