from typing import Tuple

from kontur.httptoolkitcore import Header
from kontur.httptoolkitcore.service import AsyncService
from kontur.httptoolkitcore.transport import AsyncHttpxTransport


class AsyncHttpxService(AsyncService):
    def __init__(
        self,
        url: str,
        headers: Tuple[Header, ...] = (),
    ) -> None:
        super().__init__(transport=AsyncHttpxTransport(url), headers=headers)
