import json
import re

import requests
from bs4 import BeautifulSoup

class VideoCDN:
    def __init__(self, url):
        self.url = url
        self.HEADERS = {
            "referer": "https://videocdn.tv/",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        }
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

    def getVideoUrl(self):
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
                    match = re.search(r"dn=(.*?)\[(.*?)\]", video_file)
                    if match:
                        translation_name = match.group(2)
                # Add the URL to the list of URLs
                urls[key] = f"https:{video_file}"

            # Append the data to the list
            if translations:
                data.append(
                    {
                        "id": file_id,
                        "translation_name": translation[file_id],
                        "files": urls,
                    }
                )
            else:
                data.append(
                    {"id": file_id, "translation_name": translation_name, "files": urls}
                )

        # Return the data
        return data


if __name__ == "__main__":
    data = VideoCDN("https://196622434375553.svetacdn.in/Z1VVUcly7Aoi/tv-series/2")
    print(data.getVideoUrl())
