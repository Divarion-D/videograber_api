import aplication.libs.tmdb as TMDb
import aplication.libs.kinopoisk as KP
import aplication.config as config

tmdb = TMDb.TMDb()
tmdb.api_key = config.TMDB_API_KEY
tmdb.language = "ru"

kp = KP.KP()
kp.api_key = config.KPUN_API_KEY


class Search_model:
    def __init__(self):
        pass

    # Ищемая строка
    def search(string):
        # movies = Details().tv_show(string)
        # print(movies)
        # return movies

        movies = KP.Search().search_filter(keyword="си")
        return movies
