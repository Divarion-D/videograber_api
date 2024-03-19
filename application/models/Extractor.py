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
            voidboost_data = {}
            void = voidboost(kp_id)
            translations = void.get_translations()
            for translation in translations:
                if translation["video_key"] is not None:
                    voidboost_data[translation["name"]] = void.get_movie_stream(
                        translation["video_key"]
                    )
            data["voidboost"] = voidboost_data
        if player_name == "videocdn" or player_name == "all":
            videocdn_data = {}
            videocdn = VideoCDN(kp_id, Common.CONFIG["VIDEOCDN_API"])
            for video in videocdn.getData():
                videocdn_data[video["translation_name"]] = video["files"]
            data["videocdn"] = videocdn_data
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
