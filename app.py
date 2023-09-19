import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from aplication.models.Search import Search_model


app = FastAPI()

@app.get("/")
async def root(request: Request):
    # get ip
    url = str(request.url)
    return {"info": "This is player parser", "api": url, "api_docs": url + "docs", "api_redoc": url + "redoc"}


@app.get("/search")
async def search(query: str):
    data = Search_model.search(query)
    print(data)
    return data


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.2", port=8001, reload=True)
