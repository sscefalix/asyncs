from asyncs.response import BaseResponse


class TextResponse(BaseResponse):
    def __init__(self, status_code: int, content: str) -> None:
        self._content = content

        super().__init__(content_type="text/html", status_code=status_code, content=content)

    @property
    def content(self) -> str:
        return self._content

    def get_response(self) -> str:
        return self.content
