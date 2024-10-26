from typing import Any, Dict

from asyncs.response import BaseResponse


class JSONResponse(BaseResponse):
    def __init__(self, status_code: int, content: dict[str, Any]) -> None:
        self._content = content

        super().__init__(content_type="application/json", status_code=status_code, content=content)

    @property
    def content(self) -> dict[str, Any]:
        return self._content

    def get_response(self) -> dict[str, Any]:
        return self._content
