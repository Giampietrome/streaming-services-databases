# streaming-services-databases
A script for downloading the movie database from all the streaming services.

Uses ['Unofficial JustWatch API'](https://github.com/dawoudt/JustWatchAPI) and ['Cinemagoer'](https://github.com/cinemagoer/cinemagoer).

1) Select the country.
2) Select the provider.
3) Select what to get:  original_title, local_title, imdb_id,
                        relase_year, runtime, production_countries,
                        generes, directors, writers, actors.

The database will be saved in a csv file with "|" as separator. As example there is a db with the first 50 movies of the italian Amazon Prime Video catalog.

The download will be LONG, the JustWatch api is very fast so to avoid to trigger constantly 'the api rate limit error', there are a 10 seconds timer every time this type of error occurs and a slow_mode if there is too much load on the api.

If you are using linux change 'cls' in 'clear', in the final_class file.
This is my frist python project.
