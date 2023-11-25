import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from application.models.Search import Search_model


app = FastAPI()


@app.exception_handler(Exception)
async def value_error_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )


@app.get("/")
async def root(request: Request):
    # get ip
    url = str(request.url)
    return {
        "info": "This is player parser",
        "api": url,
        "api_docs": url + "docs",
        "api_redoc": url + "redoc",
    }


@app.get("/search")
async def search(query: str):
    return Search_model().search(query)


@app.get("/details")
async def details(kp_id: int):
    return Search_model().details(kp_id)


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.2", port=8001, reload=True)
