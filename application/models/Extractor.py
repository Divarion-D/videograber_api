from application.libs.videocdn import VideoCDN
from application.libs.voidboost import voidboost
import application.models.Common as Common


class Extractor_Model:
    def __init__(self):
        self.vodboost = voidboost()
        self.videocdn = VideoCDN(Common.CONFIG["VIDEOCDN_API"])

    def get_player_movie(self, kp_id, player_name):
        data = {}
        if player_name == "voidboost" or player_name == "all":
            self.vodboost.setKPid(kp_id)
            data["voidboost"] = self.vodboost.Movie_link()
        if player_name == "videocdn" or player_name == "all":
            self.videocdn.setKPid(kp_id)
            data["videocdn"] = self.videocdn.Movie_link()
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
