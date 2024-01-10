from pymongo import MongoClient
import yaml
import json
import requests

with open('config.yaml') as f:
    CONFIG = yaml.load(f, Loader=yaml.FullLoader)

def send_api(path, method):
    API_HOST = "https://api.themoviedb.org"
    url = API_HOST + path
    headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'Accept': '*/*'}
    params = {'api_key': CONFIG["api"]["tmdb"]["key"], 'language': 'ko-KR'}
    body = {
	"api_key": CONFIG["api"]["tmdb"]["key"],
	"language": "ko-KR"
    }
    
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers, params=params)
        elif method == 'POST':
            response = requests.post(url, headers=headers, data=json.dumps(body))
        print("response status %r" % response.status_code)
        
        movies = []
        for movie in json.loads(response.text)["results"]:
            movies.append({"_id" if k == "id" else k:v for k,v in movie.items()})
            
        return movies
        
    except Exception as ex:
        print(ex)
        
        
movies = send_api("/3/movie/now_playing", "GET")

MONGO_CONFIG = CONFIG['database']['mongo']

client = MongoClient(host=MONGO_CONFIG['host'], port=MONGO_CONFIG['port'], username=MONGO_CONFIG['username'], password=MONGO_CONFIG['password'])
movieList = client.MovieHAM.movieList

movieList.insert_many(movies, ordered=False)