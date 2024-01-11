import json
import requests
import yaml
import datetime

with open('config.yaml') as f:
    CONFIG = yaml.load(f, Loader=yaml.FullLoader)

def movie_init(page):
    url = "https://api.themoviedb.org/3/discover/movie"
    headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'Accept': '*/*'}
    
    params = {'api_key': CONFIG["api"]["tmdb"]["key"], 'language': 'ko-KR', 'region': 'KR', 'page': page, 'release_date.gte': '2023-12-31', 'release_date.lte': '2024-01-01'}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        movies = json.loads(response.text)
        
        movieList = []
            
        for movie in json.loads(response.text)["results"]:
            movieList.append({"_id" if k == "id" else k:v for k,v in movie.items()})        
    
        if(movies['total_pages'] > page):
            movieList += movie_init(page+1)

        return movieList
        
    except Exception as ex:
        print(ex)        

print(datetime.date(2019, 1, 7).strftime("%Y-%m-%d"))