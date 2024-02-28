import json
import re
import requests
from bs4 import BeautifulSoup


CACHE_TIME = 3600


class videocdnException(Exception):
    pass


class VideoCDN:
    def __init__(self, api_key: str):
        self.HEADERS = {
            "referer": "https://videocdn.tv/",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        }
        self.api_key = api_key

    def setKPid(self, kp_id):
        self.kp_id = str(kp_id)
        self.data = self.getData()

    def getData(self):
        if self.api_key == "":
            raise videocdnException("Error: VideoCDN API key is not set.")
        self.url = f"https://videocdn.tv/api/short?api_token={self.api_key}&kinopoisk_id={self.kp_id}"
        response_data = json.loads(self.getPage().text)
        self.url = f"http:{response_data['data'][0]['iframe_src']}"
        self.page = self.getPage()
        self.soup = self.getSoup()

    def getPage(self):
        for _ in range(3):
            try:
                response = requests.get(self.url, headers=self.HEADERS)
                if response.status_code == 200:
                    return response
                else:
                    print("Error occurred while getting page: ", response.status_code)
            except Exception as e:
                print("Error occurred while getting page: ", e)
        return None

    def getSoup(self):
        return BeautifulSoup(self.page.text, "html.parser")

    def URLconvertStrToList(self, string):
        # Split the URLs and create a dictionary with placeholders
        url_list = string.split(",")
        videos_url = {}
        for url in url_list:
            resolution = url.split("//")[0].replace("[", "").replace("p]", "")
            video_url = "http://" + url.split("//")[1]
            videos_url[resolution] = video_url
        return videos_url

    def Movie_link(self) -> dict:
        data = {}
        download = self.soup.select_one("#fs")
        translations = self.soup.find(class_="translations")
        if translations:
            translation = {}
            for option in translations.find_all("option"):
                translation[option.attrs["value"]] = option.get_text().strip()
        if download:
            json_data = download.get("value")
            if json_data:
                json_data = json.loads(json_data)
                for translation_id, translation_data in json_data.items():
                    # Add the translation name to the dictionary
                    data[translation[translation_id]] = self.URLconvertStrToList(
                        translation_data
                    )
        return data

    def TvSeasons(self) -> dict:
        seasons_data = []
        try:
            download = self.soup.select_one("#fs")
            if download:
                json_data = download.get("value")
                if json_data:
                    json_data = json.loads(json_data)
                    for translation_id, translation_data in json_data.items():
                        if translation_id == "0":
                            continue
                        translation_name = (
                            translation_data[0]["folder"][0]["comment"]
                            .split("<br><i>")[1]
                            .split("</i>")[0]
                        )
                        seasons = [
                            {
                                translation["id"]: [
                                    video["id"].split("_")[1]
                                    for video in translation["folder"]
                                ]
                            }
                            for translation in translation_data
                        ]
                        seasons_data.append(
                            {"name": translation_name, "seasons": seasons}
                        )
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        return seasons_data

    def TV_link(self, season, series) -> dict:
        data = {}
        download = self.soup.select_one("#fs")
        if download:
            json_data = download.get("value")
            if json_data:
                json_data = json.loads(json_data)
                for translation_id, translation_data in json_data.items():
                    for season_data in translation_data:
                        for folder_data in season_data["folder"]:
                            if folder_data["id"] == f"{season}_{series}":
                                translation_name = (
                                    folder_data["comment"]
                                    .split("<br><i>")[1]
                                    .split("</i>")[0]
                                )
                                data[translation_name] = self.URLconvertStrToList(
                                    folder_data["file"]
                                )
                                break
        return data


if __name__ == "__main__":
    data = VideoCDN("Api_key")
    # data.setKPid("491724")
    # print(data.Movie_link())

    data.setKPid("749374")
    # print(data.TvSeasons())
    print(data.TV_link(1, 1))
