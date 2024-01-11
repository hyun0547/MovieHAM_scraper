from pymongo import MongoClient
import yaml

with open('/home/movieham/movieScraper/config.yaml') as f:
    CONFIG = yaml.load(f, Loader=yaml.FullLoader)

MONGO_CONFIG = CONFIG['database']['mongo']

client = MongoClient(host=MONGO_CONFIG['host'], port=MONGO_CONFIG['port'], username=MONGO_CONFIG['username'], password=MONGO_CONFIG['password'])
movies = client.MovieHAM.movies
people = client.MovieHAM.people

def mongo_insert_many_movies(docs):
    if(len(docs) != 0):
        movies.insert_many(docs, ordered=False)

def mongo_insert_many_people(docs):
    if(len(docs) != 0):
        people.insert_many(docs, ordered=False)
