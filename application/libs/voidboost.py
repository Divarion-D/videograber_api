import base64
import json
import re
import sqlite3
import time
from ast import literal_eval
from itertools import product

import requests

CACHE_TIME = 3600


class voidboost:
    def __init__(self):
        self.error = False
        # connect to db
        self.dbcon = sqlite3.connect("voidboost.db")
        self.dbcon.row_factory = self._dict_factory
        self.dbcurs = self.dbcon.cursor()

        # other variables
        self.video_key = None
        self.season = None
        self.series = None
        self._add_table_bd()

    def _dict_factory(self, cursor, row):
        d = {}  # Создаем пустой словарь
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]  # Заполняем его значениями
        return d

    def _add_table_bd(self):
        # create table voidboost
        self.dbcurs.execute(
            """CREATE TABLE IF NOT EXISTS voidboost ("id" INTEGER PRIMARY KEY AUTOINCREMENT, "kp_id" TEXT, "translation_name" TEXT, "video_key" TEXT)"""
        )
        self.dbcurs.execute(
            """CREATE TABLE IF NOT EXISTS voidboost_cache ("id" INTEGER PRIMARY KEY AUTOINCREMENT, "kp_id" TEXT, "time" TEXT)"""
        )
        self.dbcurs.execute(
            """CREATE TABLE IF NOT EXISTS voidboost_seasons ("id" INTEGER PRIMARY KEY AUTOINCREMENT, "kp_id" TEXT, "video_key" TEXT, "translation_name" TEXT, "seasons" json)"""
        )
        self.dbcon.commit()

    def get_movie_stream(self, translations_key=None):
        self.video_key = translations_key
        self.html = self._get_player("movie_key")

        return self._get_file_url()

    def get_series_stream(self, translations_key=None, season=None, series=None):
        self.video_key = translations_key
        self.set_season_and_series(season, series)
        self.html = self._get_player("serial_key")

        return self._get_file_url()

    def set_season_and_series(self, season=None, series=None):
        self.season = str(season)
        self.series = str(series)

    def _get_player(self, player_type="id"):
        if player_type == "id":
            url = "https://voidboost.tv/embed/%s" % self.kp_id
        elif player_type == "movie_key":
            url = "https://voidboost.tv/movie/{}/iframe".format(self.video_key)
        elif player_type == "serial_key":
            if self.season is not None:
                url = "https://voidboost.tv/serial/{}/iframe?s={}&e={}".format(
                    self.video_key, self.season, self.series
                )
            else:
                url = "https://voidboost.tv/serial/{}/iframe".format(self.video_key)
        else:
            return None
        try:
            data = requests.get(url).text
            return data
        except Exception as e:
            self.error = True
            print(f"Error in voidboost: \n{e}\n")
            return None

    def _clearTrash(self, data):
        # Create a list of characters to be removed from the data
        trashList = ["@", "#", "!", "^", "$"]
        # Create an empty list to store the generated codes
        trashCodesSet = []
        # Generate codes with 2 and 3 characters from the trashList
        for i in range(2, 4):
            startchar = ""
            for chars in product(trashList, repeat=i):
                data_bytes = startchar.join(chars).encode("utf-8")
                trashcombo = base64.b64encode(data_bytes)
                trashCodesSet.append(trashcombo)
        # Split the data into an array and join it back as a string
        arr = data.replace("#2", "").split("//_//")
        trashString = "".join(arr)
        # Replace the generated codes in the string with empty strings
        for i in trashCodesSet:
            temp = i.decode("utf-8")
            trashString = trashString.replace(temp, "")
        # Decode the string using base64
        finalString = base64.b64decode(f"{trashString}==")
        # Try to decode the string using utf-8, if it fails use cp1251
        try:
            return finalString.decode("utf-8")
        except UnicodeDecodeError:
            return finalString.decode("cp1251")

    def _marge_url(self, arr):
        stream = {}
        for i in arr:
            # Split the string to extract the desired values
            res = i.split("[")[1].split("]")[0]
            video = i.split("[")[1].split("]")[1].split(" or ")[1]
            # Store the values in the 'stream' dictionary
            stream[res] = video
        return stream

    def _get_file_url(self):
        try:
            # Search for the 'file' value within the 'html' string
            file = re.search(r"'file': '(.+?)'", self.html).group(1)
            # Remove unnecessary characters and split the string
            file_decode = self._clearTrash(file).split(",")
            # Merge the extracted values into a dictionary
            return self._marge_url(file_decode)
        except Exception:
            return None

    def _check_cache(self):
        cache = self.dbcurs.execute(
            f"SELECT * FROM `voidboost` WHERE `kp_id` = {self.kp_id}"
        ).fetchone()
        if not cache:
            cache = 0
        else:
            cache = cache["time"]
        curent_time = int(time.time())
        if curent_time - CACHE_TIME < int(cache):
            return True
        else:
            self.dbcurs.execute(
                f"DELETE FROM `voidboost_cache` WHERE `kp_id` = {self.kp_id}"
            )
            self.dbcurs.execute(f"DELETE FROM `voidboost` WHERE `kp_id` = {self.kp_id}")
            self.dbcon.commit()
            return False

    def _update_cache(self):
        cache = self.dbcurs.execute(
            f"SELECT * FROM `voidboost` WHERE `kp_id` = {self.kp_id}"
        ).fetchone()
        if cache:
            self.dbcurs.execute(
                f"UPDATE `voidboost_cache` SET `time` = {int(time.time())} WHERE `kp_id` = {self.kp_id}"
            )
            self.dbcon.commit()
        else:
            self.dbcurs.execute(
                f"INSERT INTO `voidboost_cache` (`kp_id`, `time`) VALUES ({self.kp_id}, {int(time.time())})"
            )
            self.dbcon.commit()

    def get_translations(self):
        if self.error is True:
            return None

        translations_data = []

        trans_bd = self.dbcurs.execute(
            f"SELECT * FROM `voidboost` WHERE `kp_id` = {self.kp_id}"
        ).fetchall()

        if trans_bd and self._check_cache:
            for translation in trans_bd:
                translations_data.append(
                    {
                        "video_key": translation["video_key"],
                        "name": translation["translation_name"],
                    }
                )
        else:
            # Remove the specified HTML tag and its contents
            translations = self.html.replace(
                '<option data-token="" data-d="" value="0">Перевод</option>', ""
            )

            # Find all occurrences of the specified HTML tag and extract the required data
            translations = re.findall(
                r'<option data-token="(.+?)" data-d="" value="(.+?)">(.+?)</option>',
                translations,
                re.MULTILINE,
            )

            # Process each translation and store the required data in a dictionary
            for translation in translations:
                video_key, translation_id, translation_name = translation
                if translation_name == "-":
                    translation_name = "Оригинал"

                self.dbcurs.execute(
                    f"INSERT INTO `voidboost` (`kp_id`, `translation_name`, `video_key`) VALUES ({self.kp_id}, '{translation_name}', '{video_key}')"
                )
                self.dbcon.commit()

                translations_data.append(
                    {
                        "video_key": video_key,
                        "name": translation_name,
                    }
                )
            self._update_cache()
        return translations_data

    def _replace_quality(self, data: dict):
        replace_key = {
            "240p": "240",
            "360p": "360",
            "480p": "480",
            "720p": "720",
            "1080p": "1080",
            "2160p": "2160",
        }

        new_data = dict((replace_key[key], value) for (key, value) in data.items())
        return new_data

    def setKPid(self, kp_id):
        self.kp_id = str(kp_id)
        self.html = self._get_player()

    def TvSeasons(self, translations_key=None, v_key=False):
        if self.error is True:
            return None

        seasons = []
        if translations_key is None:
            seasons_bd = self.dbcurs.execute(
                f"SELECT * FROM `voidboost_seasons` WHERE `kp_id` = {self.kp_id}"
            ).fetchall()
            if seasons_bd and self._check_cache:
                for season in seasons_bd:
                    if v_key is True:
                        seasons.append(
                            {
                                "name": season["translation_name"],
                                "video_key": season["video_key"],
                                "seasons": literal_eval(season["seasons"]),
                            }
                        )
                    else:
                        seasons.append(
                            {
                                "name": season["translation_name"],
                                "seasons": literal_eval(season["seasons"]),
                            }
                        )
            else:
                translations = self.get_translations()
                # Get the first translation
                for i in range(len(translations)):
                    self.video_key = translations[i]["video_key"]
                    self.html = self._get_player("serial_key")
                    seasons_data = re.search(
                        r"var seasons_episodes =(.+?);", self.html
                    ).group(1)
                    # str dict to dict covert
                    seasons_data = json.loads(seasons_data)

                    seasons.append(
                        {
                            "name": translations[i]["name"],
                            # "video_key": self.video_key,
                            "seasons": seasons_data,
                        }
                    )
                    self.dbcurs.execute(
                        f"INSERT INTO `voidboost_seasons` (`kp_id`, `video_key`, `translation_name`, `seasons`) VALUES ({self.kp_id}, '{self.video_key}', '{translations[i]['name']}', '{json.dumps(seasons_data)}')"
                    )
                    self.dbcon.commit()

                self._update_cache()
        else:
            self.video_key = translations_key
            self.html = self._get_player("serial_key")
            seasons_data = re.search(r"var seasons_episodes =(.+?);", self.html).group(
                1
            )
            # str dict to dict covert
            seasons_data = json.loads(seasons_data)

            seasons.append(
                {
                    "name": translations[i]["name"],
                    # "video_key": self.video_key,
                    "seasons": seasons_data,
                }
            )

        return seasons

    def TV_link(self, season_number, episode_number):
        data = {}
        # get all translation video key
        seasons_bd = self.dbcurs.execute(
            f"SELECT * FROM `voidboost_seasons` WHERE `kp_id` = {self.kp_id}"
        ).fetchall()
        if seasons_bd and self._check_cache:
            for season in seasons_bd:
                video_file = self.get_series_stream(
                    season["video_key"], season_number, episode_number
                )
                if video_file:
                    data[season["translation_name"]] = self._replace_quality(video_file)
        else:
            translations = self.get_translations()
            for translation in translations:
                video_file = self.get_series_stream(
                    translation["video_key"], season_number, episode_number
                )
                if video_file:
                    data[translation["name"]] = self._replace_quality(video_file)

        return data

    def Movie_link(self):
        data = {}
        translations = self.get_translations()
        for translation in translations:
            video_file = self.get_movie_stream(translation["video_key"])
            if video_file:
                data[translation["name"]] = self._replace_quality(video_file)
        return data


if __name__ == "__main__":
    data = voidboost()
    # data.setKPid("491724")
    # print(data.Movie_link())

    data.setKPid("5270353")
    # print(data.TvSeasons())
    print(data.TV_link(1, 1))
