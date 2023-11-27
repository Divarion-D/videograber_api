import uvicorn
import argparse
import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from application.models.Search import Search_model
from application.models.Extractor import Extractor_Model
# import application.models.Common as Common


app = FastAPI()
# Common.add_table_bd()


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


@app.get("/movie/videos")
async def get_movie_videos(kp_id: int, player: str = "all"):
    return Extractor_Model().get_player_movie(kp_id, player)


# @app.get("/translation")
# async def get_videos_translation(kp_id: int, player: str = "all"):
#     return Extractor_Model().get_videos_translation(kp_id, player)


@app.get("/tvseries/seasons")
async def get_tvseries_seasons(kp_id: int, player: str = "all"):
    return Extractor_Model().get_seasons_tvseries(kp_id, player)


@app.get("/tvseries/videos")
async def get_tvseries_videos(kp_id: int, season: int, series: int, player: str = "all"):
    return Extractor_Model().get_player_tvseries(kp_id, player, season, series)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-ip", help="ip address of the server")
    parser.add_argument("-port", help="port of the server")
    
    args = parser.parse_args()
    
    if args.ip:
        os.environ["IP"] = args.ip
    if args.port:
        os.environ["PORT"] = args.port

    ip = os.environ.get("IP", "0.0.0.0")
    port = os.environ.get("PORT", "8000")

    uvicorn.run("app:app", host=ip, port=int(port), reload=True)