from time import time
from typing import Callable, Awaitable, Any, Coroutine, TYPE_CHECKING

from aiohttp.web_request import Request as AioRequest
from aiohttp.web_response import Response, json_response

from asyncs import Request, RequestMethod, Logger
from asyncs.response import BaseResponse, JSONResponse, TextResponse

if TYPE_CHECKING:
    from asyncs import Asyncs


class _AsyncsRouter:
    def __init__(self):
        super().__init__()

        self._get_routes: dict[str, Callable[[Request], Awaitable[BaseResponse]]] = {}
        self._post_routes: dict[str, Callable[[Request], Awaitable[BaseResponse]]] = {}
        self._put_routes: dict[str, Callable[[Request], Awaitable[BaseResponse]]] = {}
        self._delete_routes: dict[str, Callable[[Request], Awaitable[BaseResponse]]] = {}

        self._not_found_handler = None

        self.logger = Logger()

        self._app = None

    def set_app(self, app: "Asyncs") -> None:
        self._app = app

    def get_app(self) -> "Asyncs":
        return self._app

    def get(self, path: str) -> Callable[
        [Callable[[Request], Awaitable[BaseResponse]]], Callable[[Request], Awaitable[BaseResponse]]]:
        def decorator(func: Callable[[Request], Awaitable[BaseResponse]]) -> Callable[
            [Request], Awaitable[BaseResponse]]:
            self._get_routes[path] = func

            return func

        return decorator

    def post(self, path: str) -> Callable[
        [Callable[[Request], Awaitable[BaseResponse]]], Callable[[Request], Awaitable[BaseResponse]]]:
        def decorator(func: Callable[[Request], Awaitable[BaseResponse]]) -> Callable[
            [Request], Awaitable[BaseResponse]]:
            self._post_routes[path] = func

            return func

        return decorator

    def put(self, path: str) -> Callable[
        [Callable[[Request], Awaitable[BaseResponse]]], Callable[[Request], Awaitable[BaseResponse]]]:
        def decorator(func: Callable[[Request], Awaitable[BaseResponse]]) -> Callable[
            [Request], Awaitable[BaseResponse]]:
            self._put_routes[path] = func

            return func

        return decorator

    def delete(self, path: str) -> Callable[
        [Callable[[Request], Awaitable[BaseResponse]]], Callable[[Request], Awaitable[BaseResponse]]]:
        def decorator(func: Callable[[Request], Awaitable[BaseResponse]]) -> Callable[
            [Request], Awaitable[BaseResponse]]:
            self._delete_routes[path] = func

            return func

        return decorator

    @property
    def not_found(self) -> Callable[
        [Callable[[Request], Awaitable[BaseResponse]]], Callable[[Request], Awaitable[BaseResponse]]]:
        def decorator(func: Callable[[Request], Awaitable[BaseResponse]]) -> Callable[
            [Request], Awaitable[BaseResponse]]:
            self._not_found_handler = func

            return func

        return decorator

    @staticmethod
    def _response(response: BaseResponse) -> Response:
        if isinstance(response, JSONResponse):
            return json_response(data=response.get_response(), status=response.status_code,
                                 content_type=response.content_type, headers=response.headers)

        return Response(status=response.status_code, content_type=response.content_type, body=response.get_response(),
                        headers=response.headers)

    def _handle(self, path: str, method: RequestMethod, func: Callable[[Request], Awaitable[BaseResponse]]) -> Callable[
        [Request], Coroutine[Any, Any, Response]]:
        async def handle_request(req: AioRequest) -> Response:
            start = time()

            request = Request(RequestMethod[req.method], req.url.path, req.url.query_string,
                              {k: v for k, v in req.headers.items()})

            if self._app is not None:
                for middleware in self._app.middlewares:
                    await middleware.process_request(request, func)

            response = await func(request)

            self.logger.http_request(path, method, response.status_code, (time() * 1000) - (start * 1000))

            return self._response(response)

        return handle_request

    async def _handle_not_found(self, request: AioRequest) -> Response:
        if self._not_found_handler:
            response = await self._not_found_handler(request)
        else:
            response = TextResponse(404, f"Path {request.path} not found.")

        return self._response(response)


class Router(_AsyncsRouter):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
