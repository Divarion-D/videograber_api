,#!/usr/bin/env python3
#// 
#// Class and Function List:
#// Function list:
#// - add_player()
#// - generate_random_stringing()
#// - parse()
#// - bazon_search()
#// - ustore_search()
#// - movie_graber()
#//
if (not php_defined("BASEPATH")):
    print("No direct script access allowed")
    sys.exit()

class Graber_model(CI_Model):
    def __init__(self):
        
        
        super().__init__()
        php_date_default_timezone_set(laron_config("timezone"))
        self.load.model("tmdb_model")
    # end def __init__
    #// 
    #// Узнаем сколько времени выполнялся скрипт и сколько потребовал памяти
    #// $timer = microtime(true);
    #// $memory = memory_get_usage();
    #// 
    #// скрипты
    #// 
    #// echo 'Скрипт был выполнен за ' . (microtime(true) - $timer) . ' секунд';
    #// echo 'Скушано памяти: ' . (memory_get_usage() - $memory) . ' байт';
    #// 
    #// 
    #// 
    #// 
    #// add_player.
    #// 
    #// @author Divarion-D
    #// @since  v0.0.1
    #// @version    v1.0.0  Thursday, April 1st, 2021.
    #// @param  mixed   $id
    #// @param  mixed   $url
    #// @param  mixed   $type
    #// @param  mixed   $label
    #// @return void
    #//
    def add_player(self, id_=None, url_=None, type_=None, order_=None):
        
        
        file_data_["stringeam_key"] = self.generate_random_stringing()
        file_data_["videos_id"] = id_
        file_data_["file_source"] = type_
        file_data_["source_type"] = "link"
        file_data_["file_url"] = url_
        file_data_["label"] = ""
        file_data_["order"] = order_
        file_data_["other_player"] = 1
        self.db.insert("video_file", file_data_)

    def generate_random_stringing(self, length_=12):      
        string = ""
        characters= php_array_merge(range("a", "z"), range("0", "9"))
        max_ = php_count(characters) - 1
        i_ = 0
        while i_ < length_:
            
            rand_ = mt_rand(0, max_)
            string += characters[rand_]
            i_ += 1
        # end while
        return string
        
    #// 
    #// videocdn_get.
    #// 
    #// @author Divarion-D
    #// @since  v0.0.1
    #// @version    v1.0.0  Thursday, April 1st, 2021.
    #// @param  mixed   $query
    #// @param  mixed   $type
    #// @return mixed
    #//
    def videocdn_get(self, query_=None, type_=None):
        apiToken_ = laron_config("videocdn_api")
        #// Собираем API запрос
        url_ = "https://videocdn.tv/api/" + type_ + "?api_token=" + apiToken_ + "&" + http_build_query(query_)
        #// Делаем запрос
        ch_ = curl_init()
        curl_setopt(ch_, CURLOPT_URL, url_)
        curl_setopt(ch_, CURLOPT_HEADER, 0)
        curl_setopt(ch_, CURLOPT_RETURNTRANSFER, 1)
        curl_setopt(ch_, CURLOPT_FAILONERROR, 1)
        results_ = curl_exec(ch_)
        curl_close(ch_)
        #// Расшифровываем JSON ответ
        if (php_isset(lambda : query_["field"])):
            sear_ = query_["field"]
        else:
            sear_ = "ru_title"
        
        json_ = php_json_decode(results_, True)
        if (php_isset(lambda : json_["data"])) and json_["data"] != None:
            if (php_isset(lambda : json_["data"][0])):
                if json_["data"][0] != None:
                    for json_ in json_["data"]:
                        if self.normalize(json_[sear_]) == self.normalize(query_["query"]):
                            #// Заносим их в более понятный масив для дальнейшей работы с ним
                            json_["media"] = Array()
                            #// удаляем лишний мусор
                            json_["translations"] = Array()
                            #// удаляем лишний мусор
                            json_["episodes"] = Array()
                            #// удаляем лишний мусор
                            response_["status"] = "true"
                            response_["data"] = json_
                            break
                        else:
                            response_["status"] = "false"
                        
                    
                else:
                    response_["status"] = "false"
                
            else:
                response_["status"] = "false"
            
        else:
            response_["status"] = "false"
        
        return php_json_encode(response_)

    #// 
    #// kodik_search.
    #// 
    #// @author Daliman
    #// @since  v0.0.1
    #// @version    v1.0.0  Wednesday, September 4th, 2020.
    #// @param  mixed   $query
    #// @return mixed
    #// $query = ['imdb_id' => 'tt2570292', 'limit'=> 1]; //поиск по imdb_id
    #// $query = ['title' => 'Аватар', 'year' => 2004]; //поиск по title
    #// $query = ['kinopoisk_id' => '1009278', 'limit'=> 1]; //поиск по kp_id
    #// $query = ['shikimori_id' => '39247', 'limit'=> 1]; //поиск по shikimori_id
    #//
    def kodik_search(self, query_=None):
        
        
        api_key_ = laron_config("kodik_api")
        get_ = self.common_model.url_get_contents("https://kodikapi.com/search?token=" + api_key_ + "&" + http_build_query(query_))
        json_ = php_json_decode(get_, True)
        if json_ != None or json_ != "":
            if json_["total"] != 0:
                json_["status"] = "true"
                return json_
            else:
                return Array({"status": "false"})

        else:
            return Array({"status": "false"})

    #// 
    #// parse.
    #// 
    #// @author Daliman
    #// @since  v0.0.1
    #// @version    v1.0.0  Wednesday, November 18th, 2020.
    #// @param  mixed   $query
    #// @return mixed
    #//
    def parse(self, query_=None):
        
        
        url_ = "https://ahoy.yohoho.online/?cache" + rand(100, 999)
        headers_ = Array("Host: ahoy.yohoho.online", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0", "Accept: application/json, text/javascript, */*; q=0.01", "Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3", "Content-Type: application/x-www-form-urlencoded; charset=UTF-8", "Origin: http://galabot.local", "Connection: keep-alive", "Referer: http://galabot.local/", "Pragma: no-cache", "Cache-Control: no-cache", "TE: Trailers")
        ch_ = curl_init()
        curl_setopt(ch_, CURLOPT_URL, url_)
        curl_setopt(ch_, CURLOPT_HTTPHEADER, headers_)
        curl_setopt(ch_, CURLOPT_SSL_VERIFYPEER, False)
        curl_setopt(ch_, CURLOPT_SSL_VERIFYHOST, False)
        curl_setopt(ch_, CURLOPT_RETURNTRANSFER, 1)
        curl_setopt(ch_, CURLOPT_POST, 1)
        curl_setopt(ch_, CURLOPT_POSTFIELDS, http_build_query(query_))
        output_ = curl_exec(ch_)
        curl_close(ch_)
        grab_ = php_json_decode(output_, True)
        data_ = Array()
        if (php_isset(lambda : grab_["collaps"]["iframe"])):
            url_mov_ = grab_["collaps"]["iframe"]
            #// Парсим содержимое ссылки
            html_ = self.common_model.get_content(url_mov_)
            php_preg_match("#<title>(.+?)</title>#su", html_, name_)
            #// Ишем название
            if (php_isset(lambda : name_[1])):
                name_ = name_[1]
            else:
                name_ = name_
            
            data_["status"] = "true"
            data_["url"] = url_mov_
            data_["name"] = name_
        else:
            data_["status"] = "false"
        
        return data_
    # end def parse
    #// 
    #// bazon.
    #// 
    #// @author Daliman
    #// @since  v0.0.1
    #// @version    v1.0.0  Thursday, July 15th, 2021.
    #// @param  mixed   $query
    #// @return void
    #// 
    #// $guery = array('title' => 'Чернобыль 2019'); //поиск по titile
    #// $guery = array('kp' => '1227803'); //поиск по kpid
    #//
    def bazon_search(self, query_=None):
        
        
        api_key_ = laron_config("bazon_api")
        get_ = self.common_model.url_get_contents("https://bazon.cc/api/search?token=" + api_key_ + "&" + http_build_query(query_))
        json_ = php_json_decode(get_, True)
        if json_ != None or json_ != "":
            if (not (php_isset(lambda : json_["error"]))):
                json_["results"][0]["status"] = "true"
                return json_["results"][0]
            else:
                return Array({"status": "false"})
            
        else:
            return Array({"status": "false"})
        
    # end def bazon_search
    #// 
    #// videocdn.
    #// 
    #// @author Divarion-D
    #// @since  v0.0.1
    #// @version    v1.0.0  Thursday, April 1st, 2021.
    #// @param  mixed   $data
    #// @param  mixed   $type
    #// @return mixed
    #// 
    #// $query = ['query' => tt1798268, 'field' => 'imdb_id']; поиск по imdb_id
    #// $query = ['query' => 50598, 'field' => 'kinopoisk_id']; поиск по kpid
    #// $query = ['query' => 'герой', 'year' => 2002]; поиск по названию и году
    #// 
    def videocdn_search(self, query_=None, type_data_=None):
        
        
        if type_data_ == "movie":
            #// Проверка для фильмов
            for type_ in Array("movies", "animes"):
                data_ = php_json_decode(self.videocdn_get(query_, type_), True)
                if data_["status"] == "true":
                    return data_
                
            
            return Array({"status": "false"})
        else:
            #// Проверка для сериалов
            for type_ in Array("anime-tv-series", "show-tv-series", "tv-series"):
                data_ = php_json_decode(self.videocdn_get(query_, type_), True)
                if data_["status"] == "true":
                    return data_
                
            
            return Array({"status": "false"})
        
    # end def videocdn_search
    #// 
    #// ustore_search.
    #// 
    #// @author Daliman
    #// @since  v0.0.1
    #// @version    v1.0.0  Monday, July 12th, 2021.
    #// @param  mixed   $query
    #// @return void
    #// 
    #// $query = ['f' => 'search_by_id', 'id' => 'tt0094675', 'where' => 'imdb']; поиск по imdb_id
    #// $query = ['f' => 'search_by_id', 'id' => '868526', 'where' => 'kinopoisk']; поиск по kpid
    #// $query = ['f' => 'search_by_title', 'title' => '300 Спартанцев']; поиск по названию
    #//
    def ustore_search(self, query_=None):
        
        
        api_key_ = laron_config("ustore_api")
        get_ = self.common_model.url_get_contents("http://apidevel.ustore.bz/?" + http_build_query(query_) + "&hash=" + api_key_)
        json_ = php_json_decode(get_, True)
        if json_ != None or json_ != "":
            if (not (php_isset(lambda : json_["status"]))):
                if (not php_array_key_exists("404", json_)):
                    json_[0]["status"] = "true"
                    return json_[0]
                else:
                    return Array({"status": "false"})
                
            else:
                return Array({"status": "false"})
            
        else:
            return Array({"status": "false"})
        
    # end def ustore_search
    #// 
    #// search_for_matches.
    #// 
    #// @author Daliman
    #// @since  v0.0.1
    #// @version    v1.0.0  Thursday, September 30th, 2021.
    #// @param  mixed   $array
    #// @return mixed
    #//
    def search_for_matches(self, array_=None):
        
        
        for id_,element_ in array_.items():
            if gettype(element_) != "integer" and gettype(element_) != "stringing":
                log_message("error", php_json_encode(array_) + " element: '" + id_ + "' [" + gettype(element_) + "]")
            
        
        result_ = php_array_count_values(array_)
        out_ = None
        if php_count(array_) != 0:
            if php_count(array_) == 1:
                for id_,cnt_ in result_.items():
                    out_ = id_
                
                cnt_ = 0
            else:
                for id_,cnt_ in result_.items():
                    if cnt_ > 1:
                        out_ = id_
                    
                    cnt_ = 0
                
            
        
        return out_
    # end def search_for_matches
    #// 
    #// Номализатор для названий
    #// 
    #// @author Daliman
    #// @since  v0.0.1
    #// @version    v1.0.0  Thursday, September 30th, 2021.
    #// @param  mixed   $text
    #// @return mixed
    #//
    def normalize(self, text_=None):
        
        
        text_ = php_trim(text_)
        text_ = php_mb_stringtolower(text_)
        text_ = php_stringreplace("Ñ", "Ðµ", text_)
        return text_
    # end def normalize
    #// 
    #// bazon_validate.
    #// 
    #// @author Daliman
    #// @since  v0.0.1
    #// @version    v1.0.0  Thursday, September 30th, 2021.
    #// @param  mixed   $movie
    #// @param  mixed   $json
    #// @return void
    #//
    def bazon_validate(self, movie_=None, json_=None):
        
        
        year_ = date_parse(movie_["release"])["year"]
        #// Получаем год выпуска (2020)
        if year_ == 0:
            year_ = None
        
        if json_["status"] != "false":
            if self.normalize(json_["info"]["orig"]) == movie_["title_en"] or self.normalize(json_["info"]["rus"]) == movie_["title"]:
                if json_["info"]["year"] == year_:
                    return True
                
            
        
    # end def bazon_validate
    #// 
    #// videocdn_validate.
    #// 
    #// @author Daliman
    #// @since  v0.0.1
    #// @version    v1.0.0  Monday, October 18th, 2021.
    #// @param  mixed   $movie
    #// @param  mixed   $json
    #// @return void
    #//
    def videocdn_validate(self, movie_=None, json_=None):
        
        
        if movie_["release"] != None:
            year_ = date_parse(movie_["release"])["year"]
        
        #// Получаем год выпуска (2020)
        if year_ == 0:
            year_ = None
        
        if json_["status"] != "false":
            if movie_["is_tvseries"] == 0:
                json_data_ = json_["data"]["released"]
            else:
                json_data_ = json_["data"]["start_date"]
            
            if self.normalize(json_["data"]["orig_title"]) == movie_["title_en"] or self.normalize(json_["data"]["ru_title"]) == movie_["title"]:
                if movie_["imdbid"] != None or movie_["imdbid"] != "" or movie_["imdbid"] != "N/A":
                    if json_["data"]["imdb_id"] == movie_["imdbid"]:
                        return True
                    else:
                        if date_parse(json_data_)["year"] == year_:
                            return True
                        
                    
                else:
                    if date_parse(json_data_)["year"] == year_:
                        return True
                    
                
            
        
    # end def videocdn_validate
    #// 
    #// ustore_validate.
    #// 
    #// @author Daliman
    #// @since  v0.0.1
    #// @version    v1.0.0  Thursday, September 30th, 2021.
    #// @param  mixed   $movie
    #// @param  mixed   $json
    #// @return void
    #//
    def ustore_validate(self, movie_=None, json_=None):
        
        
        year_ = date_parse(movie_["release"])["year"]
        #// Получаем год выпуска (2020)
        if year_ == 0:
            year_ = None
        
        title_ustore_ = movie_["title_en"] + " (" + year_ + ")"
        if json_["status"] != "false":
            if self.normalize(php_substring(stringrchr(json_["title"], "/"), 1)) == title_ustore_ or self.normalize(php_stringistring(json_["title"], " / ", True)) == movie_["title"] or self.normalize(json_["title"]) == movie_["title"]:
                if movie_["imdbid"] != None or movie_["imdbid"] != "" or movie_["imdbid"] != "N/A":
                    if json_["imdb_id"] == movie_["imdbid"]:
                        return True
                    else:
                        if json_["year"] == year_:
                            return True
                        
                    
                else:
                    if json_["year"] == year_:
                        return True
                    
                
            
        
    # end def ustore_validate
    #// 
    #// kodik_validate.
    #// 
    #// @author Daliman
    #// @since  v0.0.1
    #// @version    v1.0.0  Thursday, September 30th, 2021.
    #// @param  mixed   $movie
    #// @param  mixed   $json
    #// @return void
    #//
    def kodik_validate(self, movie_=None, json_=None):
        
        
        year_ = date_parse(movie_["release"])["year"]
        #// Получаем год выпуска (2020)
        if year_ == 0:
            year_ = None
        
        if json_["status"] != "false":
            for rez_ in json_["results"]:
                if self.normalize(rez_["title_orig"]) == movie_["title_en"] or self.normalize(rez_["title"]) == movie_["title"]:
                    if rez_["year"] == year_:
                        json_ = rez_
                        json_["status"] = "true"
                        return json_
                        break
                    
                
            
        
    # end def kodik_validate
    #// 
    #// player_parser.
    #// Парсер для поиска в разных базах
    #// 
    #// @author Daliman
    #// @since  v0.0.2
    #// @version    v1.0.0  Thursday, July 16th, 2021.
    #// @version    v1.0.1  Thursday, September 30th, 2021.
    #// @version    v1.0.2  Saturday, October 2nd, 2021.
    #// @version    v1.0.3  Monday, October 18th, 2021.
    #// @param  mixed   $query
    #// @param  mixed   $type   'tv' or 'movie
    #// @return void
    #//
    def player_parser(self, query_=None, type_=None):
        
        
        #// $query = ["videos_id" => 18124 ];
        self.db.where(query_)
        self.db.order_by("videos_id", "DESC")
        self.db.limit(20)
        query_video_ = self.db.get("videos").result_array()
        for movie_ in query_video_:
            kp_id_bazon_ = kp_id_ustore_ = kp_id_kodik_ = kp_id_videocdn_ = num_player_ = 0
            imdbid_ = None
            movie_["title"] = self.normalize(movie_["title"])
            movie_["title_en"] = self.normalize(movie_["title_en"])
            year_ = date_parse(movie_["release"])["year"]
            #// Получаем год выпуска (2020)
            if year_ == 0:
                year_ = None
            
            title_grab_ = movie_["title"] + " / " + movie_["title_en"] + " (" + year_ + ")"
            #// Собираем данные для запроса (Название/title (2020))
            title_bazon_ = movie_["title"] + " " + year_
            #// Собираем данные для запроса (Название 2020)
            title_ustore_ = movie_["title_en"] + " (" + year_ + ")"
            #// Ищем по imdb_id если он есть
            if movie_["imdbid"] == None or movie_["imdbid"] == "":
                ustore_ = self.ustore_search(Array({"f": "search_by_title", "title": title_bazon_}))
                kodik_ = self.kodik_search(Array({"title": movie_["title"], "year": year_}))
                videocdn_ = self.videocdn_search(Array({"query": movie_["title"], "year": year_}), type_)
            else:
                ustore_ = self.ustore_search(Array({"f": "search_by_id", "id": movie_["imdbid"], "where": "imdb"}))
                kodik_ = self.kodik_search(Array({"imdb_id": movie_["imdbid"], "limit": 1}))
                videocdn_ = self.videocdn_search(Array({"query": movie_["imdbid"], "field": "imdb_id"}), type_)
            
            bazon_ = self.bazon_search(Array({"title": title_bazon_}))
            #// Присваиваем kp_id для каждого результата
            if self.bazon_validate(movie_, bazon_):
                kp_id_bazon_ = bazon_["kinopoisk_id"]
            
            if self.ustore_validate(movie_, ustore_):
                kp_id_ustore_ = ustore_["kinopoisk_id"]
            
            if self.videocdn_validate(movie_, videocdn_):
                kp_id_videocdn_ = videocdn_["data"]["kinopoisk_id"]
            
            kodik_ = self.kodik_validate(movie_, kodik_)
            if kodik_ != None and (php_isset(lambda : kodik_["kinopoisk_id"])):
                kp_id_kodik_ = kodik_["kinopoisk_id"]
            
            if movie_["kpid"] == None:
                #// Ищем kp_id во всех результатах
                kp_id_ar_ = Array()
                if kp_id_bazon_ != 0 or kp_id_bazon_ != None:
                    php_array_push(kp_id_ar_, kp_id_bazon_)
                
                if kp_id_ustore_ != 0 or kp_id_ustore_ != None:
                    php_array_push(kp_id_ar_, kp_id_ustore_)
                
                if kp_id_ustore_ != 0 or kp_id_ustore_ != None:
                    php_array_push(kp_id_ar_, kp_id_videocdn_)
                
                if kp_id_kodik_ != 0 or kp_id_kodik_ != None:
                    php_array_push(kp_id_ar_, kp_id_kodik_)
                
                kp_id_ = self.search_for_matches(kp_id_ar_)
            else:
                kp_id_ = movie_["kpid"]
            
            #// Начинаем искать по kp_id
            imdb_id_array_ = Array()
            if kp_id_ != None:
                if kp_id_bazon_ != kp_id_:
                    bazon_ = self.bazon_search(Array({"kp": kp_id_}))
                
                if kp_id_ustore_ != kp_id_:
                    ustore_ = self.ustore_search(Array({"f": "search_by_id", "id": kp_id_, "where": "kinopoisk"}))
                
                if kp_id_videocdn_ != kp_id_:
                    videocdn_ = self.videocdn_search(Array({"query": kp_id_, "field": "kinopoisk_id"}), type_)
                
                if kp_id_kodik_ != kp_id_:
                    kodik_ = self.kodik_search(Array({"kinopoisk_id": kp_id_, "limit": 1}))
                    kodik_ = self.kodik_validate(movie_, kodik_)
                
            
            #// Ищем imdb
            if kodik_ != None and (php_isset(lambda : kodik_["imdb_id"])):
                php_array_push(imdb_id_array_, kodik_["imdb_id"])
            
            if self.ustore_validate(movie_, ustore_) and ustore_["imdb_id"] != "N/A":
                php_array_push(imdb_id_array_, ustore_["imdb_id"])
            
            if self.videocdn_validate(movie_, videocdn_) and videocdn_["data"]["imdb_id"] != "N/A" and videocdn_["data"]["imdb_id"] != "":
                php_array_push(imdb_id_array_, videocdn_["data"]["imdb_id"])
            
            badplayer_ = self.db.get_where("video_file", Array({"videos_id": movie_["videos_id"]})).num_rows()
            #// Удаляем старые плеера и вставляем новые
            self.db.where("videos_id", movie_["videos_id"])
            self.db.delete("video_file")
            #// Начинаем добавлять плеера
            if self.ustore_validate(movie_, ustore_):
                self.add_player(movie_["videos_id"], ustore_["iframe"], "iframe", num_player_)
                num_player_ += 1
            
            if self.bazon_validate(movie_, bazon_):
                self.add_player(movie_["videos_id"], bazon_["link"], "iframe", num_player_)
                num_player_ += 1
            
            if kodik_ != None:
                self.add_player(movie_["videos_id"], kodik_["link"], "iframe", num_player_)
                num_player_ += 1
            
            if self.videocdn_validate(movie_, videocdn_):
                self.add_player(movie_["videos_id"], videocdn_["data"]["iframe_src"], "iframe", num_player_)
                num_player_ += 1
            
            if kp_id_ != None or kp_id_ != "" or kp_id_ != 0:
                grab_ = self.parse(Array({"player": "collaps", "kinopoisk": kp_id_}))
                if grab_["status"] != "false":
                    grab_["name"] = php_substring(grab_["name"], 0, php_stringlen(movie_["title"]))
                    if self.normalize(grab_["name"]) == movie_["title"]:
                        self.add_player(movie_["videos_id"], grab_["url"], "iframe", num_player_)
                        num_player_ += 1
                    
                
            else:
                grab_ = self.parse(Array({"player": "collaps", "title": title_grab_}))
                if grab_["status"] != "false":
                    grab_["name"] = php_substring(grab_["name"], 0, php_stringlen(movie_["title"]))
                    if self.normalize(grab_["name"]) == movie_["title"]:
                        self.add_player(movie_["videos_id"], grab_["url"], "iframe", num_player_)
                        num_player_ += 1
                    
                
            
            #// Присваиваем некоторые значения фильму для последующей работы
            #// $imdbid = $this->search_for_matches($imdb_id_array);
            if num_player_ != 0:
                data_update_["publication"] = 1
                data_update_["passes"] = 0
            else:
                data_update_["publication"] = 0
                data_update_["passes"] = movie_["passes"] + 1
            
            #// if ($movie['kpid'] == '' || $movie['kpid'] == NULL) {
            #// $data_update['kpid'] = $kp_id;
            #// }
            #// 
            #// if ($imdbid != NULL) {
            #// preg_match('/^(tt[0-9])/', $imdbid, $imdbid_match);
            #// if ($imdbid_match != NULL) {
            #// if ($movie['imdbid'] == NULL || $movie['imdbid'] == '') $data_update['imdbid'] = $imdbid;
            #// }
            #// }
            #//
            type_array_ = Array()
            if type_ == "movie":
                if kodik_["status"] != "false" and kodik_ != None:
                    if php_in_array(kodik_["type"], Array("foreign-movie", "soviet-cartoon", "foreign-cartoon", "russian-cartoon", "russian-movie", "cartoon-serial", "documentary-serial", "russian-serial", "foreign-serial", "multi-part-film")):
                        php_array_push(type_array_, "movie")
                    else:
                        php_array_push(type_array_, "anime")
                    
                
            else:
                if kodik_["status"] != "false" and kodik_ != None:
                    if php_in_array(kodik_["type"], Array("cartoon-serial", "documentary-serial", " russian-serial", "foreign-serial", "multi-part-film")):
                        php_array_push(type_array_, "tv_series")
                    else:
                        php_array_push(type_array_, "anime_tv_series")
                    
                
            
            #// $data_update['video_type'] = $this->search_for_matches($type_array);
            data_update_["timeadd"] = time()
            self.db.where("videos_id", movie_["videos_id"])
            self.db.update("videos", data_update_)
            data_update_ = Array()
            #// Отладка
            print_r(" " + movie_["videos_id"] + " " + movie_["title"] + " " + year_ + " ÐÑÐ»Ð¾ " + badplayer_ + " Ð¡ÑÐ°Ð»Ð¾ " + num_player_ + " </br>")
            pass
        
    # end def player_parser
    #// 
    #// graber.
    #// Функция для наполнения сайта фильмами по id tmdb
    #// 
    #// @author Daliman
    #// @since  v0.0.1
    #// @version    v1.0.0  Wednesday, November 18th, 2020.
    #// @version    v1.0.1  Thursday, April 1st, 2021.
    #// @version    v1.0.2  Thursday, July 22nd, 2021.
    #// @param  stringing  $quantity   Default: ''
    #// @param  stringing  $to
    #// @return void
    #//
    def graber_from_id(self, quantity_="", to_="movie"):
        
        
        tmdb_id_bd_movie_ = self.db.get_where("config", Array({"title": "tmdb_id_movie"})).row().value
        tmdb_id_bd_tvseries_ = self.db.get_where("config", Array({"title": "tmdb_id_tvseries"})).row().value
        success_ = 0
        st_ = 0
        if to_ == "movie":
            #// Спец переменная для того чтобы понять на каком tmdb_id остановится
            var_ = quantity_ + tmdb_id_bd_movie_
            i_ = tmdb_id_bd_movie_ + "1"
            while i_ <= var_:
                
                rez_ = self.tmdb_model.get_by_id(i_, "movie")
                if php_count(rez_) > 0 and rez_["title"] != "" and rez_["title"] != None and rez_["poster_path"] != "" and rez_["poster_path"] != None and rez_["adult"] != "true":
                    success_ = success_ + 1
                    rez_["url"] = ""
                    #// Формируем json для админ панели
                    num_rows_ = self.db.get_where("videos", Array({"tmdbid": rez_["id"], "is_tvseries": 0})).num_rows()
                    if num_rows_ == 0:
                        #// Проверяем есть ли фильм уже в бд
                        if php_preg_match("/[Ð°-ÑÑ\\s-]+$/iu", rez_["title"]):
                            if rez_["overview"] != "" or rez_["overview"] != None:
                                self.tmdb_model.import_movie_info(rez_["id"])
                                rez_["url"] = "ÐÑÐ´ÐµÑ Ð¾Ð±ÑÐ°Ð±Ð¾ÑÐ°Ð½Ð¾ cron"
                                pass
                            else:
                                rez_["url"] = "ÐÐµÑ Ð¾Ð¿Ð¸ÑÐ°Ð½Ð¸Ñ"
                                pass
                            
                        else:
                            rez_["url"] = "ÐÐ½Ð¾ÑÑÑÐ°Ð½Ð½Ð°Ñ ÑÑÐ¹Ð½Ñ"
                            pass
                        
                    else:
                        rez_["url"] = "Ð¤Ð¸Ð»ÑÐ¼ ÑÐ¶Ðµ ÐµÑÑÑ Ð² Ð±Ð´"
                        pass
                    
                    json_ = php_json_encode(rez_)
                    search_[-1] = json_
                
                if success_ <= quantity_ and var_ == i_:
                    var_ = var_ + quantity_ - success_
                
                if success_ == quantity_:
                    tmdb_id_["value"] = rez_["id"]
                    self.db.where("title", "tmdb_id_movie")
                    self.db.update("config", tmdb_id_)
                
                i_ += 1
            # end while
        else:
            #// Спец переменная для того чтобы понять на каком tmdb_id остановится
            var_ = quantity_ + tmdb_id_bd_tvseries_
            i_ = tmdb_id_bd_tvseries_ + "1"
            while i_ <= var_:
                
                rez_ = self.tmdb_model.get_by_id(i_, "tv")
                if php_count(rez_) > 0 and rez_["name"] != "" and rez_["name"] != None and rez_["poster_path"] != "" and rez_["poster_path"] != None:
                    success_ = success_ + 1
                    rez_["url"] = ""
                    #// Формируем json для админ панели
                    num_rows_ = self.db.get_where("videos", Array({"tmdbid": rez_["id"], "is_tvseries": 1})).num_rows()
                    if num_rows_ == 0:
                        #// Проверяем есть ли сериал уже в бд
                        if php_preg_match("/[Ð°-ÑÑ\\s-]+$/iu", rez_["name"]):
                            if rez_["overview"] != "" or rez_["overview"] != None:
                                self.tmdb_model.import_tvseries_info(rez_["id"], 0)
                                rez_["url"] = "ÐÑÐ´ÐµÑ Ð¾Ð±ÑÐ°Ð±Ð¾ÑÐ°Ð½Ð¾ cron"
                                pass
                            else:
                                rez_["url"] = "ÐÐµÑ Ð¾Ð¿Ð¸ÑÐ°Ð½Ð¸Ñ"
                                pass
                            
                        else:
                            rez_["url"] = "ÐÐ½Ð¾ÑÑÑÐ°Ð½Ð½Ð°Ñ ÑÑÐ¹Ð½Ñ"
                            pass
                        
                    else:
                        rez_["url"] = "Ð¤Ð¸Ð»ÑÐ¼ ÑÐ¶Ðµ ÐµÑÑÑ Ð² Ð±Ð´"
                        pass
                    
                    json_ = php_json_encode(rez_)
                    search_[-1] = json_
                
                if success_ <= quantity_ and var_ == i_:
                    var_ = var_ + quantity_ - success_
                
                if success_ == quantity_:
                    tmdb_id_["value"] = rez_["id"]
                    self.db.where("title", "tmdb_id_tvseries")
                    self.db.update("config", tmdb_id_)
                
                i_ += 1
            # end while
        
        return search_
    # end def graber_from_id
    #// 
    #// унифицированый грабер для аналогичного грабера
    #// 
    #// @author Daliman
    #// @since  v0.0.1
    #// @version    v1.0.0  Wednesday, September 22nd, 2021.
    #// @param  mixed   $type
    #// @return void
    #//
    def graber(self, type_=None):
        
        
        self.load.model("tmdb_model")
        if type_ == "movie":
            page_ = laron_config("graber_page_movie")
            config_ = Array({"is_tv": 0, "title": "title", "page": "graber_page_movie", "type_graber": "graber_movie_type"})
        else:
            page_ = laron_config("graber_page_tvshows")
            config_ = Array({"is_tv": 1, "title": "name", "page": "graber_page_tvshows", "type_graber": "graber_tvseries_type"})
        
        type_graber_ = laron_config(config_["type_graber"])
        #// Узнаем какой грабер включен сейчас
        switch_graber_ = laron_config("auto_switch_graber")
        #// Включена ли авто переключение грабера
        for case in Switch(type_graber_):
            if case(2):
                if type_ == "movie":
                    search_data_ = self.tmdb_model.get_movies_by_year(date("Y"), page_)
                else:
                    search_data_ = self.tmdb_model.get_tvshows_by_year(date("Y"), page_)
                
                break
            
            if case(3):
                if type_ == "movie":
                    search_data_ = self.tmdb_model.get_top_rated_movies(page_)
                else:
                    search_data_ = self.tmdb_model.get_top_rated_tvshows(page_)
                
                break
            
            if case(4):
                if type_ == "movie":
                    search_data_ = self.tmdb_model.get_popular_movies(page_)
                else:
                    search_data_ = self.tmdb_model.get_popular_tvshows(page_)
                
                break
            
        
        for rez_ in search_data_:
            rez_ = php_json_decode(rez_, True)
            if rez_["poster_path"] != "" and rez_["poster_path"] != None:
                num_rows_ = self.db.get_where("videos", Array({"tmdbid": rez_["id"], "is_tvseries": config_["is_tv"]})).num_rows()
                if num_rows_ == 0:
                    if php_preg_match("/[Ð°-ÑÑ\\s-]+$/iu", rez_[config_["title"]]):
                        if type_ == "movie":
                            if rez_["adult"] != "true":
                                self.tmdb_model.import_movie_info(rez_["id"])
                            
                        else:
                            self.tmdb_model.import_tvseries_info(rez_["id"], 0)
                        
                    
                
            
        
        if page_ >= 500:
            data_["value"] = 1
            if switch_graber_ == "on":
                if type_graber_ == 4:
                    data_["value"] = 2
                else:
                    data_["value"] = type_graber_ + 1
                
                self.db.where("title", config_["type_graber"])
                self.db.update("config", data_)
            
        else:
            data_["value"] = page_ + 1
        
        self.db.where("title", config_["page"])
        self.db.update("config", data_)
    # end def graber
    #// V2.0
    #// 
    #// Function to call unofficial kinopoisk api
    #// 
    #// @param  mixed   $param  the name of the method you want to call.
    #// @param  mixed   $query  array of parameters for the request
    #// @return stringing
    #//
    def get_kpun(self, param_=None, query_=None):
        api_key_ = laron_config("kinopoisk_api")
        url_ = "https://kinopoiskapiunofficial.tech/api/v2.2/" + param_ + "?" + http_build_query(query_)
        curl_ = curl_init(url_)
        curl_setopt(curl_, CURLOPT_URL, url_)
        curl_setopt(curl_, CURLOPT_RETURNTRANSFER, True)
        headers_ = Array("accept: application/json", "X-API-KEY: " + api_key_)
        curl_setopt(curl_, CURLOPT_HTTPHEADER, headers_)
        #// for debug only!
        curl_setopt(curl_, CURLOPT_SSL_VERIFYHOST, False)
        curl_setopt(curl_, CURLOPT_SSL_VERIFYPEER, False)
        resp_ = curl_exec(curl_)
        status_code_ = curl_getinfo(curl_, CURLINFO_HTTP_CODE)
        curl_close(curl_)
        data_ = Array({"status": status_code_, "data": resp_})
        return data_


    def kinopoisk_search(self, query_data_=None):
        param_ = "films"
        movies_ = self.db.get_where("videos", query_data_).result_array()
        for movie_ in movies_:
            title_ru_bd_ = self.normalize(movie_["title"])
            title_en_bd_ = self.normalize(movie_["title_en"])
            year_bd_ = date_parse(movie_["release"])["year"]
            is_tvseries_ = movie_["is_tvseries"]
            query_ = Array({"order": "NUM_VOTE", "keyword": title_ru_bd_})
            if is_tvseries_ == 0:
                query_["type"] = "FILM"
            else:
                query_["type"] = "TV_SERIES"
            
            if movie_["imdbid"] != None:
                query_["imdbId"] = movie_["imdbid"]
            
            data_ = self.get_kpun(param_, query_)
            if data_["status"] == 200:
                data_ = php_json_decode(data_["data"], True)
                if data_["items"] > 0:
                    for video_ in data_["items"]:
                        data_update_ = Array()
                        title_ru_data_ = self.normalize(video_["nameRu"])
                        title_orig_data_ = self.normalize(video_["nameOriginal"])
                        title_en_data_ = self.normalize(video_["nameEn"])
                        if title_ru_data_ == title_ru_bd_ or title_orig_data_ == title_en_bd_ or title_en_data_ == title_en_bd_:
                            if video_["year"] == year_bd_:
                                if movie_["kpid"] != video_["kinopoiskId"]:
                                    data_update_["kpid"] = video_["kinopoiskId"]
                                
                                if movie_["imdbid"] != video_["imdbId"]:
                                    data_update_["imdbid"] = video_["imdbId"]
                                
                                data_update_["updated"] = 1
                                #// print("<pre>" . print_r($data_update, true) . "</pre>");
                                self.db.where("videos_id", movie_["videos_id"])
                                self.db.update("videos", data_update_)
                                break
                data_update_["updated"] = 1
                self.db.where("videos_id", movie_["videos_id"])
                self.db.update("videos", data_update_)
            
        

