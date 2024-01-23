import api_tmdb
import mongo_MovieHAM 


       
def now_playing_movies(page):
    
    movies = api_tmdb.get_tmdb_now_playing_movies()
    try:
        
        movieList = []    
        for movie in movies:
            movieDetail = api_tmdb.rename_field('id', '_id', api_tmdb.get_tmdb_movie_detail(movie['id']))
            movieDetail['cast'] = people_init(movie['id'])
            movieList.append(movieDetail)
    
        if(movies['total_pages'] > page):
            movieList += now_playing_movies(page+1)

        return movieList
        
    except Exception as ex:
        print(ex)        
        
        
        
def people_init(movieId):
    people = api_tmdb.get_tmdb_movie_people(movieId)
    for person in people:
        try:
            mongo_MovieHAM.mongo_insert_many_people(api_tmdb.get_tmdb_person('query', person['original_name']))
        except Exception as ex:
            print(ex)
        
    return people



mongo_MovieHAM.mongo_insert_many_movies(api_tmdb.get_tmdb_now_playing_movies(1))