import json
import re

import requests


class hdvbException(Exception):
    pass


class hdvb:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.error = False
        self.kp_id = None
        self.player_url = None
        self.HEADERS1 = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        }
        self.HEADERS2 = {
            "Referer": "https://apivb.info/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
        }
        self.HEADERS3 = {
            "Referer": "{0}",
            "x-csrf-token": "{1}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
        }

    def setKPid(self, kp_id):
        self.kp_id = str(kp_id)
        self.getData()

    def getData(self):
        if self.api_key == "":
            raise hdvbException("Error: HDVB API key is not set.")
        self.url = f"https://apivb.info/api/videos.json?token={self.api_key}&id_kp={self.kp_id}"
        data = self.getPage()
        if data is not None:
            response_data = json.loads(data.text)
            self.url = response_data[0]["iframe_url"]
            self.player_url = "https://" + self.url.split("https://")[1].split("/")[0]
            self.page = self.getPage(header=2)
        else:
            return None

    def getPage(self, header=1):
        for _ in range(3):
            try:
                if header == 1:
                    response = requests.get(self.url, headers=self.HEADERS1)
                else:
                    response = requests.get(self.url, headers=self.HEADERS2)
                if response.status_code == 200:
                    self.error = False
                    return response
                else:
                    print("Error occurred while getting page: ", response.status_code)
                    self.error = True
            except Exception as e:
                print("Error occurred while getting page: ", e)
                self.error = True
        return None

    def Movie_link(self):
        if self.error:
            return None

        manifest_links = {}
        file = self.page.text.split('let playerConfigs = {"file":"~')[1].split('",')[0]
        url = self.player_url + "/playlist/" + file + ".txt"

        self.HEADERS3["Referer"] = url
        self.HEADERS3["x-csrf-token"] = self.page.text.split('"key":"')[1].split('",')[
            0
        ]

        playlist_url = requests.post(url, headers=self.HEADERS3).text
        stream_links = requests.get(playlist_url, headers=self.HEADERS1)

        block = playlist_url.replace("index.m3u8", "")
        urls = re.compile("hls\/.*?\.m3u8").findall(stream_links.text)
        if urls:
            for url in urls:
                manifest_links[int(url.split("/")[1].split(".")[0])] = (
                    block + url.replace("./", "").replace("\n", "")
                )
        else:
            urls = re.compile("\.\/.*?\n").findall(stream_links.text)
            for url in urls:
                manifest_links[int(url.split("/")[1])] = block + url.replace(
                    "./", ""
                ).replace("\n", "")

        return {"Дубляж": manifest_links}


if __name__ == "__main__":
    data = hdvb("API_KEY")
    data.setKPid("301")
    print(data.Movie_link())
