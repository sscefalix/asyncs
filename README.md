Asyncs — Асинхронная Backend HTTP Библиотека.
================
<p style="color: darkgray;">Быстрая, асинхронная и модульная HTTP библиотека.</p>

## Начало использования

Чтобы использовать **Asyncs** установите его через pip:
### Windows
```bash
pip install asyncs
```
### Linux
```bash
pip3 install asyncs
```
\
\
После этого, создайте python файл и **импортируйте** библиотеку:
```python
from asyncs import Asyncs, Request
from asyncs.response import JSONResponse, HTMLResponse
```
## Пример использования
Это пример использования Asyncs для создания Web HTTP сервера:

```python
from asyncs import Asyncs, Request
from asyncs.response import JSONResponse, HTMLResponse

app = Asyncs()

@app.get("/{name}")
async def hello_name(request: Request) -> JSONResponse:
    name = request.path_args.get("name", "Anonymous")
    return JSONResponse(status_code=200, content={"result": f"Hello {name}!"})

@app.get("/index")
async def index(request: Request) -> HTMLResponse:
    with open("index.html", encoding="utf-8") as f:
        content = f.read()

        return HTMLResponse(status_code=200, content=content, variables={
            "request": request,
            "name": "Dmitry"
        })

if __name__ == "__main__":
    app.run(host="localhost", port=8080)
```

## Ключевые преимущества

- **Асинхронный**: Asyncs построен на основе библиотеки asyncio Python, что позволяет быстро и эффективно обрабатывать параллельные запросы.
- **Скорость**: Asyncs предназначен для быстродействия и легковесности, что делает его идеальным для высокопроизводительных веб-приложений.
- **Модульный**: Asyncs позволяет разделить приложение на несколько файлов и роутеров, что упрощает управление и поддержку больших проектов.
- **Маршрутизация**: Asyncs поддерживает маршрутизацию для GET, POST, PUT и DELETE запросов с возможностью использования переменных в пути запроса или query аргументы в запросе, что упрощает создание RESTful API.
- **Логгер**: Asyncs имеет встроенный логгер, который предоставляет подробную информацию о запросах и ответах.
- **Шаблоны**: Asyncs поддерживает HTML (Jinja2) переменные

## Документация
#### Для большей информации посетите документацию.
(Не готова)

## Лицензия

#### Asyncs лицензирован под лицензией MIT. См. LICENSE для получения более подробной информации.
