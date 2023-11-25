from urllib.parse import urlencode
import requests
import Common


class Graber_Model:
    def __init__(self):
        pass

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
