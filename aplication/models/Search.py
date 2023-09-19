from aplication.libs.tmdb import TMDb, Search, Details
from aplication.libs.kinopoisk import KP
import aplication.config as config

tmdb = TMDb()
tmdb.api_key = config.TMDB_API_KEY
tmdb.language = "ru"


class Search_model:
    def __init__(self):
        pass

    # Ищемая строка
    def search(string):
        movies = Details().tv_show(string)
        print(movies)
        return movies
