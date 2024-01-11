import json
import requests
import yaml
import datetime
import api_tmdb
import mongo_MovieHAM

with open('/home/movieham/movieScraper/config.yaml') as f:
    CONFIG = yaml.load(f, Loader=yaml.FullLoader)

def movie_init(page, sdate, edate):
    url = "https://api.themoviedb.org/3/discover/movie"
    headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'Accept': '*/*'}
    
    params = {'api_key': CONFIG["api"]["tmdb"]["key"], 'language': 'ko-KR', 'region': 'KR', 'page': page, 'release_date.gte': sdate, 'release_date.lte': edate}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        movies = json.loads(response.text)
        
        movieList = []
            
        for movie in json.loads(response.text)["results"]:
            people_init(movie['id'])
            movieList.append(api_tmdb.rename_field('id', '_id', api_tmdb.get_tmdb_movie_detail(movie['id'])))
    
        if(movies['total_pages'] > page):
            movieList += movie_init(page+1)

        return movieList
        
    except Exception as ex:
        print(ex)        
        
        
        
def people_init(movieId):
    mongo_MovieHAM.mongo_insert_many(api_tmdb.get_tmdb_movie_people(movieId))




        
two_days = datetime.timedelta(days=2)
sdate = datetime.date(2024, 1, 10)
edate = datetime.date(2024, 1, 11)

while(sdate > datetime.date(2020, 1, 1)):
    try:
        mongo_MovieHAM.mongo_insert_many(movie_init(1, sdate, edate))
    except Exception as ex:
        print(ex)
    
    sdate -= two_days
    edate -= two_days
    
