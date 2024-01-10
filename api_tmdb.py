import json
import requests
import yaml

with open('config.yaml') as f:
    CONFIG = yaml.load(f, Loader=yaml.FullLoader)

def get_tmdb_now_playing_movies():
    url = "https://api.themoviedb.org/3/movie/now_playing"
    headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'Accept': '*/*'}
    
    params = {'api_key': CONFIG["api"]["tmdb"]["key"], 'language': 'ko-KR'}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        
        movies = []
        for movie in json.loads(response.text)["results"]:
            movies.append({"_id" if k == "id" else k:v for k,v in movie.items()})
            
        return movies
        
    except Exception as ex:
        print(ex)