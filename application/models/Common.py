from yaml import FullLoader, load

from application.libs.videocdn import VideoCDN
from application.libs.voidboost import voidboost
from application.libs.hdvb import hdvb


def get_config() -> dict:
    with open("config.yaml", "r") as f:
        config = load(f, Loader=FullLoader)
    return config


CONFIG = get_config()


# Нормалиировка текста
def normalize(text):
    # trim, to lower, replace
    text = text.strip().lower().replace("ё", "е")
    return text


class Extractor_Model:
    def __init__(self):
        self.vodboost = voidboost()
        self.videocdn = VideoCDN(CONFIG["VIDEOCDN_API"])
        # self.hdvb = hdvb(CONFIG["HDVB_API"])

    def get_player_movie(self, kp_id, player_name):
        data = {}
        if player_name == "voidboost" or player_name == "all":
            self.vodboost.setKPid(kp_id)
            data["voidboost"] = self.vodboost.Movie_link()
        if player_name == "videocdn" or player_name == "all":
            self.videocdn.setKPid(kp_id)
            data["videocdn"] = self.videocdn.Movie_link()
        # if player_name == "hdvb" or player_name == "all":
        #     self.hdvb.setKPid(kp_id)
        #     data["hdvb"] = self.hdvb.Movie_link()
        return data

    def get_seasons_tvseries(self, kp_id, player_name):
        data = {}
        if player_name == "voidboost" or player_name == "all":
            self.vodboost.setKPid(kp_id)
            data["voidboost"] = self.vodboost.TvSeasons()
        if player_name == "videocdn" or player_name == "all":
            self.videocdn.setKPid(kp_id)
            data["videocdn"] = self.videocdn.TvSeasons()
        return data

    def get_player_tvseries(self, kp_id, player_name, season, series):
        data = {}
        if player_name == "voidboost" or player_name == "all":
            self.vodboost.setKPid(kp_id)
            data["voidboost"] = self.vodboost.TV_link(season, series)
        if player_name == "videocdn" or player_name == "all":
            self.videocdn.setKPid(kp_id)
            data["videocdn"] = self.videocdn.TV_link(season, series)
        return data
