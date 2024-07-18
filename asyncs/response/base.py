from typing import Any


class BaseResponse:
    def __init__(self, content_type: str, status_code: int, content: Any) -> None:
        self._content_type = content_type
        self._status_code = status_code
        self._content = content

        self._headers = {
            "Server": "Asyncs Python Web Server"
        }

    @property
    def content_type(self) -> str:
        return self._content_type

    @property
    def status_code(self) -> int:
        return self._status_code

    @property
    def content(self) -> Any:
        return self._content

    @property
    def headers(self) -> dict[str, Any]:
        return self._headers

    def get_response(self) -> Any:
        return self._content
