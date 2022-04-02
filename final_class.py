from justwatch import JustWatch
import imdb
import os
import time

clear = lambda: os.system('cls')

YEAR_RANGE = 4

GENERES = {'1': 'Action', '2': 'Animation', '3': 'Comedy', '4': 'Crime', '5': 'Documentation', '6': 'Drama',
        '7': 'Fantasy', '8': 'History', '9': 'Horror', '10': 'Family', '11': 'Music', '12': 'Thriller',
        '13': 'Romance', '14': 'Scifi', '15': 'Sport', '16': 'War', '17': 'Western', '23': 'Reality', '18': 'European'}


class Final(JustWatch, imdb.IMDbBase):
    def __init__(self, country):
        super().__init__(country=country)
        self.titles_full = []
        self.originals_full = []
        self.imdb_id_full = []
        self.productions_full = []
        self.years_full = []
        self.runtimes_full = []
        self.ratings_full = []
        self.votes_full = []
        self.writers_full = []
        self.directors_full = []
        self.actors_full = []
        self.generes_full = []
        
        self.sleeping_time = 0
        self.n_sleepings = 0
        self.n_times_slow_down = 0

        self.imdb = imdb.Cinemagoer()

    def get_film(self, id):
        try:
            self.film = self.get_title(title_id=id)
        except:
            self.too_many_requests(sleep=10)
            self.film = self.get_title(title_id=id)
        return self.film

    def get_imdb_id(self, film):
        external_ids = film["external_ids"]
        try:
            for dizionari in external_ids:
                if "imdb_latest" in dizionari["provider"]:
                        id_index = external_ids.index(dizionari)
                else:
                    if "imdb" == dizionari["provider"]:
                        id_index = external_ids.index(dizionari)
        except:
            self.imdb_id_full.append("NaN")
        else:
            try:
                id = external_ids[id_index]["external_id"]
                self.imdb_id_full.append(id)
            except:
                self.imdb_id_full.append("NaN")

    def get_runtime(self, film):
        try:
            runtime = film["runtime"]
        except:
            self.runtimes_full.append("NaN")
        else:
            self.runtimes_full.append(int(runtime))

    def get_year(self, film):
        try:
            year = film["original_release_year"]
        except:
            self.years_full.append("NaN")
        else:
            self.years_full.append(int(year))

    def get_rating_and_nvotes(self, film):
        try:
            scoring = film["scoring"]
        except:
            self.ratings_full.append("NaN")
            self.votes_full.append("NaN")
        else:

            #RATINGS
            try:
                for dizionari in scoring:
                    if "imdb:score" in dizionari["provider_type"]:
                        rating_index = scoring.index(dizionari)
            except:
                self.ratings_full.append("NaN")
            else:
                try:
                    self.ratings_full.append(scoring[rating_index]["value"])
                except:
                    self.ratings_full.append("NaN")
            
            #N_VOTES
            try:
                for dizionari in scoring:
                    if "imdb:votes" in dizionari["provider_type"]:
                        votes_index = scoring.index(dizionari)
            except:
                self.votes_full.append("NaN")
            else:
                try:
                    self.votes_full.append(scoring[votes_index]["value"])
                except:
                    self.votes_full.append("NaN")
    
    def get_production_countries(self, film):
        try:
            production_countries = film["production_countries"]
        except:
            self.productions_full.append("NaN")
        else:
            self.productions_full.append(production_countries)

    def get_original_title(self, film):
        try:
            self.originals_full.append(film["original_title"])
        except:
            self.originals_full.append("NaN")

    def get_writers_and_directors(self, film):
        try:
            credits = film["credits"]
        except: 
            self.writers_full.append("NaN")
            self.directors_full.append("NaN")
        else:

            #WRITERS FROM JUSTWATCH API
            if self.imdb_id_full[-1] == "NaN":

                try:
                    index_list = []
                    movie_writers = []
                    for dizionari in credits:
                        if "SCREENPLAY" in dizionari["role"]:
                            index_list.append(credits.index(dizionari))
                except:
                    self.writers_full.append("NaN")
                else:
                    try:
                        for index in index_list:
                            movie_writers.append(credits[index]["name"])
                    except:
                        self.writers_full.append("NaN")
                    else:
                        if movie_writers != []:
                            self.writers_full.append(movie_writers)
                        else:
                            self.writers_full.append("NaN")
            #WRITERS FROM IMDB API
            else:
                try:
                    self.get_writers_imdb_api()
                except:
                    self.too_many_requests(sleep=10)
                    self.get_writers_imdb_api

            #DIRECTORS
            try:
                index_list = []
                movie_directors= []
                for dizionari in credits:
                    if "DIRECTOR" in dizionari["role"]:
                        index_list.append(credits.index(dizionari))
            except:
                self.directors_full.append("NaN")
            else:
                try:
                    for index in index_list:
                        movie_directors.append(credits[index]["name"])
                    self.directors_full.append(list(movie_directors))
                except:
                    self.directors_full.append("NaN")

    def get_actors(self):
        try:
            self.get_actors_imdb_api()
        except:
            self.too_many_requests(sleep=10)
            self.get_actors_imdb_api()

    def get_actors_imdb_api(self):
        full_id = self.imdb_id_full[-1]
        movie_actors = []
        if full_id != "NaN":
            try:
                film = self.imdb.get_movie(full_id[2:])
            except:
                self.actors_full.append("NaN")
            else:
                try:
                    for actor in film.get("cast"):
                        actor = actor.get("name")
                        if actor not in movie_actors:
                            movie_actors.append(actor)
                except:
                    self.actors_full.append("NaN")
                else:
                    self.actors_full.append(movie_actors)
        else:
            self.actors_full.append("NaN")

    def get_output(self, all_providers, provider):
        bottom_space = list(all_providers[provider])

        if " " in bottom_space:
            bottom_space[bottom_space.index(" ")] = "_"
            self.provider_full_name = "".join(bottom_space)
        else:
            self.provider_full_name = all_providers[provider]

        return self.provider_full_name

    def year_range(self, y_startig):
        return y_startig - YEAR_RANGE

    def get_generes(self, film):
        movie_generes = []
        try:
            generes_id_list = film['genre_ids']
        except:
            self.generes_full.append("NaN") 
        else:
            for genere_id in generes_id_list:
                movie_generes.append(GENERES[f"{genere_id}"])
            self.generes_full.append(movie_generes)

    def get_writers_imdb_api(self):
        movie_writers = []
        try:
            full_id = self.imdb_id_full[-1]
            film = self.imdb.get_movie(full_id[2:])
        except:
            self.writers_full.append("NaN")
        else:
            try:
                for writer in film.get("writer"):
                    writer = writer.get("name")
                    if writer not in movie_writers:
                        if writer != None:
                            movie_writers.append(writer)
            except:
                self.writers_full.append("NaN")
            else:
                if movie_writers != []:
                    self.writers_full.append(movie_writers)
                else:
                    self.writers_full.append("NaN")

    def too_many_requests(self, sleep):
        self.sleeping_time += 10 
        self.n_sleepings += 1

        for n in range(sleep, 0, -1):
            clear() 
            print(f"Too many requests please wait.\nSleeping... {n} seconds.\nError count: {self.n_sleepings}")
            time.sleep(1) 

    def slow_down(self, max_times):
        if self.n_sleepings >= 3:
            print("SLOW MODE 0,5 second sleep")
            time.sleep(0.5) 
            self.sleeping_time += 0.5
            
        elif self.n_sleepings >= 6:
            print("SLOW MODE 1 second sleep")
            time.sleep(1)
            self.sleeping_time += 1 

        elif self.n_sleepings >= 9:
            print("SLOW MODE 1,5 second sleep")
            time.sleep(1.5)
            self.sleeping_time += 1.5 

        self.n_times_slow_down += 1
        
        if self.n_times_slow_down == max_times:
            self.n_sleepings = 0
            self.n_times_slow_down = 0

    def too_many_pages(self, results):
        if results["total_pages"] == 66:
            clear()
            print(f"PROCESS STOPPED, YEARS RANGE IS TOO BIG... (CURRENT: {YEAR_RANGE})")
            exit()
    
    def get_streaming_services(self):
        self.dict_of_providers = {}
        list_of_providers = self.get_providers()
        for provider in list_of_providers:
            self.dict_of_providers[provider['short_name']] = f"{provider['clear_name'].title()}"
        return self.dict_of_providers

    def ask_provider(self):
        provider = input("Which provider database do you want to download from? (or 'show_providers')\n: ")
        self.get_streaming_services()

        while provider not in self.dict_of_providers:
            clear()
            if provider == "show_providers":
                print(f"There are {len(self.dict_of_providers)} streaming services: \n")
                for key in self.dict_of_providers:
                    print(f"Type: '{key}', for select {self.dict_of_providers[key]}.")
            else:
                print("Please retry...")
            provider = input(" \nWhich provider database do you want to download from? (es: 'nfx', 'prv' or 'show_providers')\n: ")
        clear()
        return provider

#------------------------------------------------------------------------------- SETUP

COUNTRY_LIST = {'DZ': 'Algeria', 'AG': 'Antigua and Barbuda', 'AR': 'Argentina', 'AU': 'Australia', 'AT': 'Austria', 'BS': 'Bahamas', 'BH': 'Bahrain', 'BB': 'Barbados', 'BE': 'Belgium', 'BM': 'Bermuda', 'BO': 'Bolivia, Plurinational State of', 'BR': 'Brazil', 'BG': 'Bulgaria', 'CA': 'Canada', 'CV': 'Cape Verde', 'CL': 'Chile', 'CO': 'Colombia', 'CR': 'Costa Rica', 'CI': "Cote d'Ivoire", 'HR': 'Croatia', 'CU': 'Cuba', 'CZ': 'Czech Republic', 'DK': 'Denmark', 'DO': 'Dominican Republic', 'EC': 'Ecuador', 'EG': 'Egypt', 'SV': 'El Salvador', 'GQ': 'Equatorial Guinea', 'EE': 'Estonia', 'FJ': 'Fiji', 'FI': 'Finland', 'FR': 'France', 'GF': 'French Guiana', 'PF': 'French Polynesia', 'DE': 'Germany', 'GH': 'Ghana', 'GI': 'Gibraltar', 'GR': 'Greece', 'GT': 'Guatemala', 'GG': 'Guernsey', 'HN': 'Honduras', 'HK': 'Hong Kong', 'HU': 'Hungary', 'IS': 'Iceland', 'IN': 'India', 'ID': 'Indonesia', 'IE': 'Ireland', 'IT': 'Italy', 'JM': 'Jamaica', 'JP': 'Japan', 'JO': 'Jordan', 'KE': 'Kenya', 'KR': 'Korea, Republic of', 'KW': 'Kuwait', 'LV': 'Latvia', 'LY': 'Libya', 'LI': 'Liechtenstein', 'LT': 'Lithuania', 'MY': 'Malaysia', 'MU': 'Mauritius', 'MX': 'Mexico', 'MD': 'Moldova, Republic of', 'MC': 'Monaco', 'MA': 'Morocco', 'MZ': 'Mozambique', 'NL': 'Netherlands', 'NZ': 'New Zealand', 'NE': 'Niger', 'NG': 'Nigeria', 'NO': 'Norway', 'OM': 'Oman', 'PK': 'Pakistan', 'PA': 'Panama', 'PY': 'Paraguay', 'PE': 'Peru', 'PH': 'Philippines', 'PL': 'Poland', 'PT': 'Portugal', 'QA': 'Qatar', 'RO': 'Romania', 'RU': 'Russian Federation', 'LC': 'Saint Lucia', 'SM': 'San Marino', 'SA': 'Saudi Arabia', 'SN': 'Senegal', 'SC': 'Seychelles', 'SG': 'Singapore', 'SK': 'Slovakia', 'ZA': 'South Africa', 'ES': 'Spain', 'SE': 'Sweden', 'CH': 'Switzerland', 'TW': 'Taiwan', 'TZ': 'Tanzania, United Republic of', 'TH': 'Thailand', 'TT': 'Trinidad and Tobago', 'TN': 'Tunisia', 'TR': 'Turkey', 'TC': 'Turks and Caicos Islands', 'UG': 'Uganda', 'AE': 'United Arab Emirates', 'GB': 'United Kingdom', 'US': 'United States', 'UY': 'Uruguay', 'VE': 'Venezuela, Bolivarian Republic of', 'YE': 'Yemen', 'ZM': 'Zambia'}

INFO = {
'0': 'TITLE',
'1': 'IMDB ID',
'2': 'ORIGINAL TITLE',
'3': 'RUNTIME',
'4': 'YEAR',
'5': 'PRODUCTION COUNTRIES',
'6': 'IMDB RATING & NUMBER OF IMDB VOTES',
'7': 'DIRECTOR & WRITERS',
'8': 'GENERES',
'9': 'ACTORS'
}

info_how_to = """
The download will be LONG.

Es:
    If you need title and runtime: 2, 3
    if yoy want relase year and original title (in this order): 4, 2
    If you want cast and rating: 9, 6
    If you want everything (in this order): 'all' or 0, 1, 2, 3, 4, 5, 6, 7, 8, 9

Make sure to digit correctly the input:
number comma space number
"""

class Setup:
    def __init__(self):
        pass

    def ask_country(self):
        country = input("Which country streaming provider do you want to download from? (or 'show_countries')\n: ").upper()

        while country not in COUNTRY_LIST:
            clear()
            if country == "SHOW_COUNTRIES":
                print("Countries:\n")
                for item in COUNTRY_LIST:
                    print(f"{item}: {COUNTRY_LIST[item]}.")
            else:
                print("Please retry...")
            country = input(" \nWhich country streaming provider do you want to download from? (es: 'US', 'UK'... or 'show_countries')\n: ").upper()
        clear()
        return country

    def ask_what_to_download(self):
        asking_for = input(f"What type of informations do you want to get from the provider's database? (or 'show_info', 'all')\n: ")

        while True:
            clear()
            if asking_for == "show_info":
                print("Options:\n")
                for key in INFO:
                    print(f"{key}: {INFO[key]}")
                print(info_how_to)
                asking_for = input(f" \nWhat type of informations do you want to get from the provider's database? (or 'show_info', 'all')\n: ")
            elif asking_for == "all":
                asking_for = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            else:
                try:
                    asking_for = [int(number) for number in list(asking_for) if number != "," and number != " "]
                except:
                    clear()
                    print("Please retry...")
                else:
                    break
        return asking_for
        
    def put_underscore(self, world):
        world = list(world)
        
        for letter in world:
            if letter == " ":
                world[world.index(letter)] = "_"

        provider_full_name = "".join(world)
        return provider_full_name


