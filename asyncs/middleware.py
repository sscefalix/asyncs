from typing import Callable, Awaitable, TYPE_CHECKING

if TYPE_CHECKING:
    from asyncs import Asyncs, Request
    from asyncs.response import BaseResponse


class BaseMiddleware:
    def __init__(self, app: "Asyncs") -> None:
        self._app = app

    @property
    def app(self) -> "Asyncs":
        return self._app

    async def process_request(self, request: "Request",
                              func: Callable[["Request"], Awaitable["BaseResponse"]]) -> "BaseResponse":
        raise NotImplementedError("process_request is not implemented.")
