import requests
import os
import logging
import time

logger = logging.getLogger(__name__)


class KPException(Exception):
    pass


class KP(object):
    _session = None
    KP_API_KEY = "KP_API_KEY"
    KP_PROXIES = "KP_PROXIES"
    KP_DEBUG_ENABLED = "KP_DEBUG_ENABLED"

    def __init__(self, obj_cached=True, session=None):
        if self.__class__._session is None or session is not None:
            self.__class__._session = requests.Session() if session is None else session
        self._base = "https://kinopoiskapiunofficial.tech"
        self._remaining = 40
        self._reset = None
        self.obj_cached = obj_cached

    @property
    def proxies(self):
        proxy = os.environ.get(self.KP_PROXIES)
        if proxy is not None:
            proxy = eval(proxy)
        return proxy

    @proxies.setter
    def proxies(self, proxies):
        if proxies is not None:
            os.environ[self.KP_PROXIES] = str(proxies)

    @property
    def api_key(self):
        return os.environ.get(self.KP_API_KEY)

    @api_key.setter
    def api_key(self, api_key):
        os.environ[self.KP_API_KEY] = str(api_key)

    @property
    def debug(self):
        if os.environ.get(self.KP_DEBUG_ENABLED) == "True":
            return True
        else:
            return False

    @debug.setter
    def debug(self, debug):
        os.environ[self.KP_DEBUG_ENABLED] = str(debug)

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
            raise KPException("No API key found.")

        url = "%s%s?%s" % (
            self._base,
            action,
            params,
        )

        api_header = {"X-API-KEY": self.api_key}

        req = self.__class__._session.request(
            method, url, data=data, json=json, headers=api_header, proxies=self.proxies
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
                raise KPException(
                    "Rate limit reached. Try again in %d seconds." % sleep_time
                )

        json = req.json()

        # if "page" in json:
        #     os.environ["page"] = str(json["page"])

        # if "total_results" in json:
        #     os.environ["total_results"] = str(json["total"])

        # if "total_pages" in json:
        #     os.environ["total_pages"] = str(json["totalPages"])

        if self.debug:
            logger.info(json)

        # if status code is not 200, raise an exception
        if req.status_code != 200:
            raise KPException(req.text)

        return json


class Search(KP):
    _urls = {
        "filter": "/api/v2.2/films",
        "keyword": "/api/v2.1/films/search-by-keyword",
    }

    def __init__(self):
        super().__init__()

    def search_filter(
        self,
        order="RATING",
        type="ALL",
        ratingFrom=0,
        ratingTo=10,
        yearFrom=1000,
        yearTo=3000,
        keyword=None,
        imdbid=None,
        page=1,
    ):
        params = (
            "order=%s&type=%s&ratingFrom=%s&ratingTo=%s&yearFrom=%s&yearTo=%s&page=%s"
            % (order, type, ratingFrom, ratingTo, yearFrom, yearTo, page)
        )

        if imdbid is not None:
            params += "&imdbId=%s" % imdbid

        if keyword is not None:
            params += "&keyword=%s" % keyword

        return self._request_obj(self._urls["filter"], params=params, key="items")

    def search_by_keyword(self, keyword, page=1):
        params = "keyword=%s&page=%s" % (keyword, page)
        return self._request_obj(self._urls["keyword"], params=params, key="films")
