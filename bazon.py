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
        ## Change Existing Header
        del request.headers['Referer']  # Delete the header first
        request.headers['Referer'] = 'https://v1681235361.bazon.site/embed/695289b2e9c710dfa5bff772315bf102/91909'  # Add new header

    driver = webdriver.Chrome()
    ## Set Request Interceptor
    driver.request_interceptor = interceptor
    
    data = Bazon(url, driver)
    print(data.getVideoUrl())


curl 'https://v1681235361.bazon.site/vid/c45n/91909/480/1/1/index.m3u8?hash=b53f4bd1533c2cb6f0b8bdb3ccf0209e&expires=1681284650&domain=bazon.cc' \
  -H 'authority: v1681235361.bazon.site' \
  -H 'referer: https://v1681235361.bazon.site/embed/695289b2e9c710dfa5bff772315bf102/91909' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36' \
  --compressed


curl 'https://v1681235361.bazon.site/get_file_encoded/d31bbc54acab1724bf50906f8b8efb05' \
  -H 'authority: v1681235361.bazon.site' \
  -H 'accept: */*' \
  -H 'accept-language: ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,ms;q=0.6,zh-TW;q=0.5,zh;q=0.4' \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json; charset=UTF-8' \
  -H 'cookie: ci_session=pmvk8ba6k7kukojj6dinhji8skiq2r43' \
  -H 'origin: https://v1681235361.bazon.site' \
  -H 'pragma: no-cache' \
  -H 'referer: https://v1681235361.bazon.site/embed/e4ec000aa0622d33c046ca10ebbe1e4d' \
  -H 'sec-ch-ua: "Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36' \
  --data-raw '{"data":"PZ7R2kut73F0UaMkKnY9T6GtXI/nKxr+L7smMrmjvki57FTJMO7eybETFnojtDBjyL2BeBYmCycHIT/0opLhMMK1LfHwIPtKriWv/tUNaiOyUlDUlKjsSbqaF75KkZOl9RtpWVkTr6AJFZEVmI45GOtWUsEv1D/vE1VD2Sj6/Dw="}' \
  --compressed