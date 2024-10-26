from typing import Any

from asyncs.response import BaseResponse
from jinja2 import Template


class HTMLResponse(BaseResponse):
    def __init__(self, status_code: int, content: str, variables: dict[str, Any]) -> None:
        self._content = content
        self._variables = variables

        assert variables.get("request") is not None, "request is required argument in variables."

        super().__init__(content_type="text/html", status_code=status_code, content=content)

    @property
    def content(self) -> str:
        return self._content

    def get_response(self) -> str:
        template = Template(self._content)

        return template.render(**self._variables)
