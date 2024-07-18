from enum import Enum


class RequestMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


class Request:
    def __init__(self, method: RequestMethod, path: str, query: str, headers: dict[str, str]) -> None:
        self._method = method
        self._path = path
        self._query = query
        self._headers = headers

    @property
    def method(self) -> RequestMethod:
        return self._method

    @property
    def path(self) -> str:
        return self._path

    @property
    def query(self) -> str:
        return self._query

    @property
    def headers(self) -> dict[str, str]:
        return self._headers
