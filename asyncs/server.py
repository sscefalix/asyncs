from asyncio import run as async_run, sleep
from traceback import extract_stack
from typing import Callable, Awaitable, Any, TYPE_CHECKING, Type

from aiohttp.web_app import Application
from aiohttp.web_runner import AppRunner, TCPSite

from asyncs.middleware import BaseMiddleware
from asyncs.router import _AsyncsRouter
from asyncs import RequestMethod

if TYPE_CHECKING:
    from asyncs import Router


class Asyncs(_AsyncsRouter):
    def __init__(self, *args, on_startup: Callable[["Asyncs"], Awaitable[Any]] = None, **kwargs) -> None:
        super().__init__()

        self.set_app(self)

        self._on_startup_handler = on_startup
        self._routers: set["Router"] = set()
        self._middlewares: set[BaseMiddleware] = set()

    @property
    def middlewares(self) -> set[BaseMiddleware]:
        return self._middlewares

    async def _startup_log(self, host: str, port: int) -> None:
        self.logger.info(f"Application start on: http://{host}:{port}/")

    async def _start(self, host: str, port: int) -> None:
        app = Application()

        for path, func in self._get_routes.items():
            app.router.add_get(f"{path}", self._handle(path, RequestMethod.GET, func))

        for path, func in self._post_routes.items():
            app.router.add_post(f"{path}", self._handle(path, RequestMethod.POST, func))

        for path, func in self._put_routes.items():
            app.router.add_put(f"{path}", self._handle(path, RequestMethod.PUT, func))

        for path, func in self._delete_routes.items():
            app.router.add_delete(f"{path}", self._handle(path, RequestMethod.DELETE, func))

        app.router.add_route("*", "/{path:.*}", self._handle_not_found)

        runner = AppRunner(app=app)
        await runner.setup()

        tcp = TCPSite(runner=runner, host=host, port=port)
        await tcp.start()

        await self._on_startup_handler(self)

        while True:
            await sleep(3600)

    def include_middleware(self, middleware: Type[BaseMiddleware]) -> None:
        self._middlewares.add(middleware(self))

    def include_router(self, router: "Router") -> None:
        self._get_routes = self._get_routes | router._get_routes
        self._post_routes = self._get_routes | router._post_routes
        self._put_routes = self._get_routes | router._put_routes
        self._delete_routes = self._get_routes | router._delete_routes

        self._routers.add(router)
        router.set_app(self)

        if self._not_found_handler is None and router._not_found_handler is not None:
            self._not_found_handler = router._not_found_handler

        self.logger.info_with_line(f"Router included successfully.", extract_stack()[-2].lineno)

    def run(self, host: str = "localhost", port: int = 8080) -> None:
        async_run(self._startup_log(host, port))
        try:
            async_run(self._start(host=host, port=port))
        except KeyboardInterrupt:
            self.logger.info("Stopped.")
