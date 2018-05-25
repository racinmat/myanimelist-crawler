'''
This script only creates list of anime ids from users ratings so we have anime for all ratings and not any dangling foreign keys.
'''
import os
import pickle
from pymongo import MongoClient

mongo = MongoClient('localhost', 27017)
users_db = mongo.mal.users

anime_ids = list(users_db.aggregate([
    {'$match': {'$and': [{'loadedRatings': {'$eq': True}}, {'anime': {"$ne": None}}]}},
    {'$unwind': {'path': '$anime', 'preserveNullAndEmptyArrays': False}},
    {'$group': {'_id': '$anime.series_animedb_id'}},
]))
anime_ids = [i['_id'] for i in anime_ids]

pickleFile = 'AnimeList.rick'

print('{} unique animes written'.format(len(anime_ids)))
# this is for original getUser.py format
with open('AnimeList.txt', 'w+') as f:
    f.write('\n'.join(anime_ids))

# this is to keep users with other data, denormalized, perpared for multiple runs, for getUserJson
if os.path.exists(pickleFile):
    with open(pickleFile, 'rb') as f:
        animes = pickle.load(f)
else:
    animes = dict()

for anime_id in anime_ids:
    if anime_id in animes:
        continue
    animes[anime_id] = {'id': anime_id, 'loadedInfo': False}

with open(pickleFile, 'wb+') as f:
    pickle.dump(animes, f)
