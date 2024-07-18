Asyncs Web Libary.
================
<p style="color: darkgray;">A fast, asynchronous, and modular web framework for Python.</p>

### Getting Started

To use Asyncs, simply install it via pip:

```bash
$ pip install asyncs
```

Then, create a new Python file and import the library:
```python
from asyncs import Asyncs, Request
from asyncs.response import JSONResponse, HTMLResponse
```

Example Usage

Here's a simple example of creating a web application with Asyncs:

```python
from asyncs import Asyncs, Request
from asyncs.response import JSONResponse, HTMLResponse

app = Asyncs()

@app.get("/")
async def index(request: Request) -> JSONResponse:
    return JSONResponse(status_code=200, content={"result": "Hello World!"})

@app.get("/index")
async def index(request: Request) -> HTMLResponse:
    with open("index.html", encoding="utf-8") as f:
        content = await f.read()

        return HTMLResponse(status_code=200, content=content, variables={
            "request": request,
            "name": "Dmitry"
        })

if __name__ == "__main__":
    app.run(host="localhost", port=8080)
```

## Key Features

- Asynchronous: Asyncs is built on top of Python's asyncio library, allowing for fast and efficient handling of concurrent requests.
- Speed: Asyncs is designed to be fast and lightweight, making it perfect for high-performance web applications.
- Modular: Asyncs allows you to split your application into multiple files and routers, making it easy to manage and maintain large projects.
- Routing: Asyncs supports routing for GET, POST, PUT, and DELETE requests, making it easy to create RESTful APIs.
- Logger: Asyncs comes with a built-in logger that provides detailed information about requests and responses.

## Documentation
#### For more information on using Asyncs, please see the full documentation.

## License

#### Asyncs is licensed under the MIT License. See LICENSE for more information.