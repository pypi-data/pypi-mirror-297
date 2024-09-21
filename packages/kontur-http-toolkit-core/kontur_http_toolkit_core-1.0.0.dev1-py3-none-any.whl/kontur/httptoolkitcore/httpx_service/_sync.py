from typing import Tuple

from kontur.httptoolkitcore import Header
from kontur.httptoolkitcore.service import Service
from kontur.httptoolkitcore.transport import HttpxTransport


class HttpxService(Service):
    def __init__(
        self,
        url: str,
        headers: Tuple[Header, ...] = (),
    ) -> None:
        super().__init__(transport=HttpxTransport(url), headers=headers)
