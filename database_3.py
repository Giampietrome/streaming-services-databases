import pandas as pd
from time import time
from datetime import datetime
import final_class

start = time()
day = datetime.utcfromtimestamp(start).strftime('%Y_%m_%d')

country = final_class.Setup().ask_country()
aa = final_class.Final(country)
provider = aa.ask_provider()
asking_for = final_class.Setup().ask_what_to_download()

y_starting = 2030

while True:
    y_ending = aa.year_range(y_starting)

    if y_ending <= 1900:
        break

    try:
        results = aa.search_for_item(providers=[provider], 
                                            content_types=['movie'], 
                                            release_year_until=y_starting, 
                                            release_year_from=y_ending)

        max = int(results["total_pages"])+1
        
    except KeyError:
        final_class.clear()
        print(f"{y_starting}-{y_ending}: NO MOVIES")

    else:
        for pagina in range(0, max):

            try:
                results = aa.search_for_item(providers=[provider], 
                                                    content_types=['movie'], 
                                                    release_year_until=y_starting, 
                                                    release_year_from=y_ending, 
                                                    page=pagina)       
            except:
                aa.too_many_requests(sleep=10)
                results = aa.search_for_item(providers=[provider], 
                                                    content_types=['movie'], 
                                                    release_year_until=y_starting, 
                                                    release_year_from=y_ending, 
                                                    page=pagina)                  
            
            for n in results["items"]:
                title = n["title"]

                if title not in aa.titles_full:
                    aa.titles_full.append(title)

                    id = n["id"]
                    film = aa.get_film(id)
                    aa.get_imdb_id(film)

                    if 2 in asking_for:
                        aa.get_original_title(film)
                    if 3 in asking_for:
                        aa.get_runtime(film)
                    if 4 in asking_for: 
                        aa.get_year(film)
                    if 5 in asking_for: 
                        aa.get_production_countries(film)
                    if 6 in asking_for:
                        aa.get_rating_and_nvotes(film)
                    if 7 in asking_for:
                        aa.get_writers_and_directors(film)
                    if 8 in asking_for:
                        aa.get_generes(film)
                    if 9 in asking_for:
                        aa.get_actors()

                aa.slow_down(200)

                final_class.clear()
                state = float(results['page']/results['total_pages']*100)
                print(f"{y_starting}-{y_ending}: {round(state, 2)}%, {len(aa.titles_full)} movies.")
                print("The '%' refers to the total movies in the year range.")
                aa.too_many_pages(results)

    y_starting = y_ending

finito = {}

for item in asking_for:
    if item == 0:
        finito["TITLE"] = aa.titles_full
    elif item == 1:
        finito["ID"] = aa.imdb_id_full
    elif item == 2:
        finito["ORIGINAL_TITLE"] = aa.originals_full
    elif item == 3:
        finito["RUNTIME"] = aa.runtimes_full
    elif item == 4:
        finito["YEAR"] = aa.years_full
    elif item == 5:
        finito["PRODUCTION"] = aa.productions_full
    elif item == 6:
        finito["RATING"] = aa.ratings_full
        finito["N_VOTES"] = aa.votes_full
    elif item == 7:
        finito["DIRECTOR"] = aa.directors_full 
        finito["WRITERS"] = aa.writers_full
    elif item == 8:
        finito["GENERES"] = aa.generes_full
    elif item == 9:
        finito["ACTORS"] = aa.actors_full
    
finito = pd.DataFrame.from_dict(finito)

provider_full_name = aa.dict_of_providers[provider]
provider_full_name = final_class.Setup().put_underscore(world=provider_full_name)

finito.to_csv(f"{provider_full_name.title()}_DB_{country}_{day}.csv", index=False, sep="|")

end = time()
total = end - start

final_class.clear()
print(f"Total runtime: {round(total, 2)} seconds.")
print(f"Fetching runtime: {round(total-aa.sleeping_time, 2)} seconds.")
print(f"Sleeping runtime: {round(aa.sleeping_time, 2)} seconds.")