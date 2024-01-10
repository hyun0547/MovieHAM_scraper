import api_tmdb
import mongo_MovieHAM 
       
movies = api_tmdb.get_tmdb_now_playing_movies()

mongo_MovieHAM.mongo_insert_many(movies)

