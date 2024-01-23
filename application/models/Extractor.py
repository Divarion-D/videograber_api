from urllib.parse import urlencode
from application.libs.voidboost import voidboost
from application.libs.videocdn import VideoCDN
import requests
import application.models.Common as Common


class Extractor_Model:
    def __init__(self):
        pass

    def get_player_movie(self, kp_id, player_name):
        data = {}
        if player_name == "voidboost" or player_name == "all":
            voidboost_data = {}
            void = voidboost(kp_id)
            translations = void.get_translations()
            for translation in translations:
                if translation["video_key"] is not None:
                    voidboost_data[translation["name"]] = void.get_movie_stream(translation["video_key"])
            data["voidboost"] = voidboost_data
        if player_name == "videocdn" or player_name == "all":
            videocdn_data = {}
            videocdn = VideoCDN()
            for video in videocdn.getKPid(kp_id):
                videocdn_data[video["translation_name"]] = video["files"]
            data["videocdn"] = videocdn_data
        return data
    
    def get_seasons_tvseries(self, kp_id, player_name):
        data = {}
        if player_name == "voidboost" or player_name == "all":
            void = voidboost(kp_id)
            data["voidboost"] = void.get_seasons()
        if player_name == "videocdn" or player_name == "all":
            videocdn = VideoCDN()
            data["videocdn"] = videocdn.getKPid(kp_id)
        return data
    
    def get_player_tvseries(self, kp_id, player_name, season, series):
        data = {}
        if player_name == "voidboost" or player_name == "all":
            voidboost_data = {}
            void = voidboost(kp_id)
            seasons_data = void.get_seasons()
            for season_data in seasons_data:
                voidboost_data[season_data["name"]] = void.get_series_stream(season_data["video_key"], season, series)
            data["voidboost"] = voidboost_data
        return data






    # $query = ['imdb_id' => 'tt2570292', 'limit'=> 1]; //поиск по imdb_id
    # $query = ['title' => 'Аватар', 'year' => 2004]; //поиск по title
    # $query = ['kinopoisk_id' => '1009278', 'limit'=> 1]; //поиск по kp_id
    # $query = ['shikimori_id' => '39247', 'limit'=> 1]; //поиск по shikimori_id
    # kodik_fieldch(query={"imdb_id": "tt2570292", "year": 2004})
    def kodik_fieldch(self, query):
        req = requests.get(
            "https://kodikapi.com/fieldch?token=" + KODIK_API + "&" + urlencode(query)
        )
        json_data = req.json_data()
        if json_data is not None or json_data != "":
            if json_data["total"] != 0:
                json_data["status"] = "true"
                return json_data
            else:
                return {"status": "false"}
        else:
            return {"status": "false"}

    # $query = ['query' => tt1798268, 'field' => 'imdb_id']; поиск по imdb_id
    # $query = ['query' => 50598, 'field' => 'kinopoisk_id']; поиск по kpid
    # $query = ['query' => 'герой', 'year' => 2002]; поиск по названию и году
    # videocdn_fieldch({"query": "Спасатель", "field": "ru_title"}, "movie")
    def videocdn_fieldch(self, query, type_data):
        if type_data == "movie":
            # Check for movies
            types = ["movies", "animes"]
        else:
            # Check for TV series
            types = ["anime-tv-series", "show-tv-series", "tv-series"]

        for type in types:
            data = self.videocdn_get(query, type)
            if data.get("status") == "true":
                return data

        return None

    # делает запрос находит совпадение и возвращает ответ
    def videocdn_get(self, query, type):
        url = "https://videocdn.tv/api/{}?api_token={}&{}".format(
            type, VIDEOCDN_API, urlencode(query)
        )
        results = requests.get(url)
        json_data = results.json()

        response = {"status": "false"}
        if "data" in json_data and json_data["data"] is not None:
            for item in json_data["data"]:
                if Common.normalize(item[query["field"]]) == Common.normalize(
                    query["query"]
                ):
                    response["status"] = "true"
                    response["data"] = item
                    break
        return response
