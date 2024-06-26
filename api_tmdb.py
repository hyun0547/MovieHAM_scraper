import json
import requests
import yaml
import googletrans
from datetime import datetime

with open('/home/movieham/movieScraper/config.yaml') as f:
    CONFIG = yaml.load(f, Loader=yaml.FullLoader)



def get_tmdb_now_playing_movies(page=1):
    url = "https://api.themoviedb.org/3/movie/now_playing"
    headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'Accept': '*/*'}
    
    params = {'api_key': CONFIG["api"]["tmdb"]["key"], 'language': 'ko-KR', 'page': page}
    
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
        
        
        
def get_tmdb_movie_people(movieId):
    url = f'https://api.themoviedb.org/3/movie/{movieId}/credits'
    headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'Accept': '*/*'}
    translator = googletrans.Translator()
    
    params = {'api_key': CONFIG["api"]["tmdb"]["key"]}
    try:
        casts = []
        response = requests.get(url, headers=headers, params=params)
        
        for cast in json.loads(response.text)["cast"]:
            if(cast['name']):
                cast['name'] = translator.translate(text=cast['name'], dest='ko', src='en').text
            if(cast['character']):
                cast['character'] = translator.translate(text=cast['character'], dest='ko', src='en').text
            
            casts.append(rename_field('id', '_id', cast))
        
        return casts
    
    except Exception as ex:
        print(ex)
        
        
        
def get_tmdb_person(searchKey, searchVal):
    url = 'https://api.tmdb.org/3/search/person'
    params = {'api_key': CONFIG["api"]["tmdb"]["key"], 'language': 'ko-KR', searchKey: searchVal}
    headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'Accept': '*/*'}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        translator = googletrans.Translator()
        person = []
        
        for people in json.loads(response.text)['results']:
            if(people['name']):
                people['name'] = translator.translate(text=people['name'], dest='ko', src='en').text
                
            person.append(rename_field('id', '_id', people))
            
        return person
    
    except Exception as ex:
        print(ex)        


        
def convert_field(dict):
    return convert_date(rename_field('_id', 'id', dict))
    
def convert_date(dict):
    dict['release_date'] = datetime.strptime(dict['release_date'], '%Y-%m-%d')
    return dict
    
def rename_field(to, origin, dict):
    return {to if k == origin else k:v for k,v in dict.items()}
    

    
