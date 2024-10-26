from asyncs import Asyncs, Request
from asyncs.response import JSONResponse, HTMLResponse

app = Asyncs()

@app.get("/{name}")
async def index(request: Request) -> JSONResponse:
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
