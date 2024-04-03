import requests
from bs4 import BeautifulSoup

from seleniumwire import webdriver

import time


class Bazon:
    def __init__(self, url, driver):
        self.url = url
        self.driver = driver
        self.page = self.getPage()
        self.soup = self.getSoup()

    def getPage(self):
        for _ in range(3):
            try:
                self.driver.get(self.url)
                return self.driver
            except Exception as e:
                print("Error occurred while getting page: ", e)
        return None

    def getSoup(self):
        soup = BeautifulSoup(self.page.page_source, "html.parser")
        self.driver.close()
        return soup

    def getVideoUrl(self):
        print(self.soup)
        return f"https:{self.soup.find('video').get('src')}"


if __name__ == "__main__":
    url = "http://v1681235361.bazon.site/vid/c45n/91909/480/1/1/index.m3u8?hash=b53f4bd1533c2cb6f0b8bdb3ccf0209e&expires=1681284650&domain=bazon.cc"

    def interceptor(request):
        # Change Existing Header
        del request.headers["Referer"]  # Delete the header first
        request.headers["Referer"] = (
            "https://v1681235361.bazon.site/embed/695289b2e9c710dfa5bff772315bf102/91909"  # Add new header
        )

    driver = webdriver.Chrome()
    # Set Request Interceptor
    driver.request_interceptor = interceptor

    data = Bazon(url, driver)
    print(data.getVideoUrl())
