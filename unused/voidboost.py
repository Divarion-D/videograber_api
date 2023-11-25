import base64
from itertools import product
import requests
import re
import json


class voidboost:
    def __init__(self, kp_id=None):
        self.kp_id = kp_id
        self.video_key = None
        self.html = self._get_player()
        self.season = None
        self.series = None

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
        self.season = season
        self.series = series

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
            return False
        data = requests.get(url).text
        return data

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
        # Search for the 'file' value within the 'html' string
        file = re.search(r"'file': '(.+?)'", self.html).group(1)
        # Remove unnecessary characters and split the string
        file_decode = self._clearTrash(file).split(",")
        # Merge the extracted values into a dictionary
        return self._marge_url(file_decode)

    def get_translations(self):
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

        translations_data = []
        # Process each translation and store the required data in a dictionary
        for translation in translations:
            video_key, translation_id, translation_name = translation
            if translation_name == "-":
                translation_name = "Оригинал"

            translations_data.append(
                {
                    "video_key": video_key,
                    "name": translation_name,
                }
            )
        return translations_data

    def get_seasons(self, translations_key=None):
        seasons = []
        if translations_key is None:
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
                        "video_key": self.video_key,
                        "seasons": seasons_data,
                    }
                )
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
                    # "name": translations[i]["name"],
                    "video_key": self.video_key,
                    "seasons": seasons_data,
                }
            )

        return seasons


if __name__ == "__main__":
    # # error
    # kp_id = "55489498484"
    # void = voidboost(kp_id)
    # print(void.get_stream())

    #  print("______________________MOVIE_________________________")

    # # get all single translation
    # kp_id = "44168"
    # void = voidboost(kp_id)
    # translations = void.get_translations()
    # print(void.get_movie_stream(translations[0]["video_key"]))

    # print("____________________________________________________")
    # # get concrete translation
    # kp_id = "370"
    # void = voidboost(kp_id)
    # translations = void.get_translations()
    # # key translation
    # print(void.get_movie_stream(translations[3]["video_key"]))

    print("____________________TV_SHOW__________________________")
    # get all multi translation
    kp_id = "404900"
    void = voidboost(kp_id)
    seasons = void.get_seasons()
    data = seasons[1]
    print(void.get_series_stream(data["video_key"], "1", "5"))
