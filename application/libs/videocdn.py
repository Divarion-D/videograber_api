import json
import re

# import config as config
import requests
from bs4 import BeautifulSoup
import application.models.Common as Common


class videocdnException(Exception):
    pass


class VideoCDN:
    def __init__(self):
        self.HEADERS = {
            "referer": "https://videocdn.tv/",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        }
        self.api_key = Common.CONFIG["VIDEOCDN_API"]

    def getUrl(self, url):
        self.url = url
        self.page = self.getPage()
        self.soup = self.getSoup()
        return self.getVideo()

    def getKPid(self, kp_id):
        if self.api_key == "":
            raise videocdnException("Error: VideoCDN API key is not set.")
        self.url = f"https://videocdn.tv/api/short?api_token={self.api_key}&kinopoisk_id={kp_id}"
        response_data = json.loads(self.getPage().text)
        self.url = f"http:{response_data['data'][0]['iframe_src']}"
        self.page = self.getPage()
        self.soup = self.getSoup()
        return self.getVideo()

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

    def getVideo(self):
        """
        This function gets the video URLs from a given page.
        """
        # Get the files from the page
        downloads = self.soup.find(id="downloads")
        files = downloads.attrs["value"]

        # Get the translations from the page
        translations = self.soup.find(class_="translations")

        # Replace the backslashes with forward slashes
        files = files.replace("\/", "/")

        # Load the files as JSON
        files = json.loads(files)

        data = []

        # Extract translation names
        translation_name = ""
        if translations:
            translation = {}
            for option in translations.find_all("option"):
                translation[option.attrs["value"]] = option.get_text().strip()
            translation_name = translation

        # Loop through the files
        for file_id, file_data in files.items():
            urls = {}
            for key, video_file in file_data.items():
                # If the translation name is empty, set it to the video file
                if translation_name == "":
                    match = re.search(r"dn=(.*?)\[(.*?)\]", str(video_file))
                    if match:
                        translation_name = match.group(2)
                # Add the URL to the list of URLs
                if key in ["1080p", "720p", "480p", "360p", "240p"]:
                    urls[key] = f"https:{video_file}"
                else:
                    # Add https to url serial
                    for series in video_file:
                        for video in video_file[series]:
                            video_file[series][
                                video
                            ] = f"https:{video_file[series][video]}"
                    urls[key] = video_file

            # Append the data to the list
            if translations:
                data.append(
                    {
                        # "id": file_id,
                        "translation_name": translation[file_id],
                        "files": urls,
                    }
                )
            else:
                data.append(
                    {
                        # "id": file_id,
                        "translation_name": translation_name,
                        "files": urls,
                    }
                )
                break

        # Return the data
        return data


if __name__ == "__main__":
    data = VideoCDN()
    # print(data.getUrl("https://68175.svetacdn.in/Z1VVUcly7Aoi/tv-series/23"))
    print(data.getKPid("4647040"))
    # print(data.getKPid("994676"))
