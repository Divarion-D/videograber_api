import logging
import os
import time

import requests

try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote

try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache

logger = logging.getLogger(__name__)

# init
# tmdb = TMDb()
# tmdb.api_key = "your_api_key"
# tmdb.language = "ru"
# tmdb.proxies = {"http": "http://000000000:8080", "https": "http://000000000:8080"}
# tmdb.debug = True
#
#
# # search
# all = Search().multi("ti")
# print(movies)
#
# movies = Search().movies("titanik")
# print(movies)
#
# tv = Search().tv("simpsons")
# print(tv)
#
# # details
# details = Details().movie(1399)
# print(details)
#
# details = Details().tv(1399)
# print(details)


class TMDbException(Exception):
    pass


class TMDb(object):
    _session = None
    TMDB_API_KEY = "TMDB_API_KEY"
    TMDB_LANGUAGE = "TMDB_LANGUAGE"
    TMDB_PROXIES = "TMDB_PROXIES"
    TMDB_DEBUG_ENABLED = "TMDB_DEBUG_ENABLED"
    TMDB_CACHE_ENABLED = "TMDB_CACHE_ENABLED"
    REQUEST_CACHE_MAXSIZE = None

    def __init__(self, obj_cached=True, session=None):
        if self.__class__._session is None or session is not None:
            self.__class__._session = requests.Session() if session is None else session
        self._base = "https://api.themoviedb.org/3"
        self._remaining = 40
        self._reset = None
        self.obj_cached = obj_cached
        if os.environ.get(self.TMDB_LANGUAGE) is None:
            os.environ[self.TMDB_LANGUAGE] = "en-US"

    @property
    def proxies(self):
        proxy = os.environ.get(self.TMDB_PROXIES)
        if proxy is not None:
            proxy = eval(proxy)
        return proxy

    @proxies.setter
    def proxies(self, proxies):
        if proxies is not None:
            os.environ[self.TMDB_PROXIES] = str(proxies)

    @property
    def api_key(self):
        return os.environ.get(self.TMDB_API_KEY)

    @api_key.setter
    def api_key(self, api_key):
        os.environ[self.TMDB_API_KEY] = str(api_key)

    @property
    def language(self):
        return os.environ.get(self.TMDB_LANGUAGE)

    @language.setter
    def language(self, language):
        os.environ[self.TMDB_LANGUAGE] = language

    @property
    def cache(self):
        if os.environ.get(self.TMDB_CACHE_ENABLED) == "False":
            return False
        else:
            return True

    @cache.setter
    def cache(self, cache):
        os.environ[self.TMDB_CACHE_ENABLED] = str(cache)

    @staticmethod
    @lru_cache(maxsize=REQUEST_CACHE_MAXSIZE)
    def cached_request(method, url, data, json, proxies):
        return requests.request(method, url, data=data, json=json, proxies=proxies)

    def cache_clear(self):
        return self.cached_request.cache_clear()

    @property
    def debug(self):
        if os.environ.get(self.TMDB_DEBUG_ENABLED) == "True":
            return True
        else:
            return False

    @debug.setter
    def debug(self, debug):
        os.environ[self.TMDB_DEBUG_ENABLED] = str(debug)

    def _request_obj(
        self,
        action,
        params="",
        call_cached=True,
        method="GET",
        data=None,
        json=None,
        key=None,
    ):
        if self.api_key is None or self.api_key == "":
            raise TMDbException("No API key found.")

        url = "%s%s?api_key=%s&%s&language=%s" % (
            self._base,
            action,
            self.api_key,
            params,
            self.language,
        )

        if self.cache and self.obj_cached and call_cached and method != "POST":
            req = self.cached_request(method, url, data, json, self.proxies)
        else:
            req = self.__class__._session.request(
                method, url, data=data, json=json, proxies=self.proxies
            )

        headers = req.headers

        if "X-RateLimit-Remaining" in headers:
            self._remaining = int(headers["X-RateLimit-Remaining"])

        if "X-RateLimit-Reset" in headers:
            self._reset = int(headers["X-RateLimit-Reset"])

        if self._remaining < 1:
            current_time = int(time.time())
            sleep_time = self._reset - current_time

            if self.wait_on_rate_limit:
                logger.warning("Rate limit reached. Sleeping for: %d" % sleep_time)
                time.sleep(abs(sleep_time))
                return self._request_obj(
                    action, params, call_cached, method, data, json, key
                )
            else:
                raise TMDbException(
                    "Rate limit reached. Try again in %d seconds." % sleep_time
                )

        json = req.json()

        if "page" in json:
            os.environ["page"] = str(json["page"])

        if "total_results" in json:
            os.environ["total_results"] = str(json["total_results"])

        if "total_pages" in json:
            os.environ["total_pages"] = str(json["total_pages"])

        if self.debug:
            logger.info(json)
            logger.info(self.cached_request.cache_info())

        if "errors" in json:
            raise TMDbException(json["errors"])

        if "success" in json and json["success"] is False:
            raise TMDbException(json["status_message"])

        return json


class Search(TMDb):
    _urls = {
        "multi": "/search/multi",
        "movie": "/search/movie",
        "tv_shows": "/search/tv",
    }

    def __init__(self):
        super().__init__()

    def multi(self, term, adult=None, region=None, page: int = 1) -> dict:
        params = "query=%s&page=%s" % (quote(term), page)
        if adult is not None:
            params += "&include_adult=%s" % "true" if adult else "false"
        if region is not None:
            params += "&region=%s" % quote(region)
        return self._request_obj(self._urls["multi"], params=params, key="results")

    def movies(
        self, term, adult=None, region=None, year=None, release_year=None, page=1
    ):
        """
        Search for movies.
        :param term: str
        :param adult: bool
        :param region: str
        :param year: int
        :param release_year: int
        :param page: int
        :return:
        """
        params = "query=%s&page=%s" % (quote(term), page)
        if adult is not None:
            params += "&include_adult=%s" % "true" if adult else "false"
        if region is not None:
            params += "&region=%s" % quote(region)
        if year is not None:
            params += "&year=%s" % year
        if release_year is not None:
            params += "&primary_release_year=%s" % release_year

        return self._request_obj(self._urls["movie"], params=params, key="results")

    def tv_shows(self, term, adult=None, release_year=None, page=1):
        """
        Search for a TV show.
        :param term: str
        :param adult: bool
        :param release_year: int
        :param page: int
        :return:
        """
        params = "query=%s&page=%s" % (quote(term), page)
        if adult is not None:
            params += "&include_adult=%s" % "true" if adult else "false"
        if release_year is not None:
            params += "&first_air_date_year=%s" % release_year
        return self._request_obj(self._urls["tv_shows"], params=params, key="results")


class Details(TMDb):
    _urls = {
        "movie": "/movie/%s",
        "tv_show": "/tv/%s",
    }

    _appender = {
        "movies": ["external_ids"],
        "tv_shows": ["external_ids"],
    }

    def __init__(self):
        super().__init__()

    def movie(self, movie_id):
        """
        Get the primary information about a movie.
        :param movie_id: int
        :return:
        """
        if self._appender["movies"]:
            appenders = []
            for appender in self._appender["movies"]:
                if appender not in appenders:
                    appenders.append(appender)
            appenders_str = ",".join(appenders)

            params = "&append_to_response=%s" % appenders_str

        return self._request_obj(self._urls["movie"] % movie_id, params=params)

    def tv_show(self, tv_id):
        """
        Get the primary information about a TV show.
        :param tv_id: int
        :return:
        """
        if self._appender["tv_shows"]:
            appenders = []
            for appender in self._appender["tv_shows"]:
                if appender not in appenders:
                    appenders.append(appender)
            appenders_str = ",".join(appenders)

            params = "&append_to_response=%s" % appenders_str

        return self._request_obj(self._urls["tv_show"] % tv_id, params=params)
