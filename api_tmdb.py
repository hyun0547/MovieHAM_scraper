import json
import requests
import yaml

with open('/home/movieham/movieScraper/config.yaml') as f:
    CONFIG = yaml.load(f, Loader=yaml.FullLoader)

def get_tmdb_now_playing_movies():
    url = "https://api.themoviedb.org/3/movie/now_playing"
    headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'Accept': '*/*'}
    
    params = {'api_key': CONFIG["api"]["tmdb"]["key"], 'language': 'ko-KR'}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        
        movies = []
        for movie in json.loads(response.text)["results"]:
            get_tmdb_movie_detail(movie['id'])
            movies.append(rename_field("id", "_id", movie))
            
        return movies
        
    except Exception as ex:
        print(ex)


        
def get_tmdb_movie_detail(movieId):
    url = f'https://api.themoviedb.org/3/movie/{movieId}'
    headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'Accept': '*/*'}
    
    params = {'api_key': CONFIG["api"]["tmdb"]["key"], 'language': 'ko-KR'}
    try:
        response = requests.get(url, headers=headers, params=params)
        return json.loads(response.text)
        
    except Exception as ex:
        print(ex)


        
def rename_field(origin, to, dict):
    return {to if k == origin else k:v for k,v in dict.items()}
    
    