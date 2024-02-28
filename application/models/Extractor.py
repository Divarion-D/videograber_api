from application.libs.videocdn import VideoCDN
from application.libs.voidboost import voidboost
import application.models.Common as Common


class Extractor_Model:
    def __init__(self):
        pass

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
            void = voidboost(kp_id)
            data["voidboost"] = void.getSeasons()
        if player_name == "videocdn" or player_name == "all":
            videocdn = VideoCDN(kp_id, Common.CONFIG["VIDEOCDN_API"])
            data["videocdn"] = videocdn.getSeasons()
        return data

    def get_player_tvseries(self, kp_id, player_name, season, series):
        data = {}
        if player_name == "voidboost" or player_name == "all":
            voidboost_data = {}
            void = voidboost(kp_id)
            seasons_data = void.getSeasons(v_key=True)
            for season_data in seasons_data:
                voidboost_data[season_data["name"]] = void.get_series_stream(
                    season_data["video_key"], season, series
                )
            data["voidboost"] = voidboost_data
        if player_name == "videocdn" or player_name == "all":
            videocdn = VideoCDN(kp_id, Common.CONFIG["VIDEOCDN_API"])
            data["videocdn"] = videocdn.getVideos()
        return data
