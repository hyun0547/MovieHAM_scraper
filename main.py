import requests
import json
import yaml

with open('config.yaml') as f:
    CONFIG = yaml.load(f, Loader=yaml.FullLoader)

def send_api(path, method):
    print(CONFIG["api"]["tmdb"]["key"])
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
        print("response text %r" % response.text)
    except Exception as ex:
        print(ex)
  

# 호출 예시
send_api("/3/movie/now_playing", "GET")

