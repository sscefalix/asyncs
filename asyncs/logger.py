from datetime import datetime

from asyncs import RequestMethod


class Logger:
    def __init__(self) -> None:
        ...

    @staticmethod
    def info(msg: str) -> None:
        time = datetime.now().strftime("%H:%M:%S.%f")[:-3]

        print(f"INFO:    {time} | {msg}")

    @staticmethod
    def info_with_line(msg: str, line: int) -> None:
        time = datetime.now().strftime("%H:%M:%S.%f")[:-3]

        print(f"INFO:    {time} LINE:{line} | {msg}")

    def http_request(self, path: str, method: RequestMethod, status_code: int, execution_time: float) -> None:
        self.info(f"""[HTTP] "{method.value} {path}" {status_code} ({execution_time:.2f} ms)""")
