from pymongo import MongoClient
import yaml
import json

with open('config.yaml') as f:
    CONFIG = yaml.load(f, Loader=yaml.FullLoader)

MONGO_CONFIG = CONFIG['database']['mongo']

client = MongoClient(host=MONGO_CONFIG['host'], port=MONGO_CONFIG['port'], username=MONGO_CONFIG['username'], password=MONGO_CONFIG['password'])
movies = client.MovieHAM.movies

movies.drop()

#sample
with open('./sample_movie.json', 'r') as f:
    movie = json.load(f)

# id => _id rename key
movie = {"_id" if k == "id" else k:v for k,v in movie.items()}
movies.insert_one(movie)

print(movies.find_one())


