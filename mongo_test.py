from pymongo import MongoClient
import yaml

with open('config.yaml') as f:
    CONFIG = yaml.load(f, Loader=yaml.FullLoader)

MONGO_CONFIG = CONFIG['database']['mongo']

client = MongoClient(host=MONGO_CONFIG['host'], port=MONGO_CONFIG['port'], username=MONGO_CONFIG['username'], password=MONGO_CONFIG['password'])

db = client.MovieHAM

print(db)