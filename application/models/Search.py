import application.libs.kinopoisk as KP
import application.config as config
import application.models.Common as Common

kp = KP.KP()
kp.api_key = config.KPUN_API_KEY


class Search_model:
    def __init__(self):
        pass

    # Ищемая строка
    def search(self, string):
        kp_data = KP.Search().search_by_keyword(string)["films"]
        data = []

        for i in range(len(kp_data)):
            # if nameRu is set
            if "nameRu" in kp_data[i]:
                find_title = Common.normalize(kp_data[i]["nameRu"]).find(
                    Common.normalize(string)
                )

                if find_title != -1:
                    orig_title = kp_data[i]["nameEn"] if "nameEn" in kp_data[i] else ""
                    year = kp_data[i]["year"] if "year" in kp_data[i] else ""
                    description = (
                        kp_data[i]["description"] if "description" in kp_data[i] else ""
                    )
                    poster = (
                        kp_data[i]["posterUrl"] if "posterUrl" in kp_data[i] else ""
                    )
                    country = (
                        kp_data[i]["countries"] if "countries" in kp_data[i] else ""
                    )
                    genre = kp_data[i]["genres"] if "genres" in kp_data[i] else ""

                    details = {
                        "kp_id": kp_data[i]["filmId"],
                        "title": kp_data[i]["nameRu"],
                        "original_title": orig_title,
                        "year": year,
                        "description": description,
                        "type": kp_data[i]["type"],
                        "poster": poster,
                        "country": country,
                        "genre": genre,
                    }
                    data.append(details)
        return data

    def details(self, id):
        return KP.Search().get_details(id)
