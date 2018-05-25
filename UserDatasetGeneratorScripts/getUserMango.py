'''
This script can be used to download user dataset from [**Myanimelist**](https://myanimelist.net/) using an API, [**Kuristina**](https://github.com/TimboKZ/kuristina).

For CSV output, please use the pickleToCsv script.
'''

# importing libraries
import pickle

import pymongo
import requests
import json
import sys

from myanimelist import utilities
from pymongo import MongoClient

from utils import AnimeRecord


def anime_record_to_named_tuple(anime_rec):
    anime_object = AnimeRecord(
        series_animedb_id=anime_rec['series_animedb_id'],  # this is MAL anime ID, enough to identify it
        my_watched_episodes=anime_rec['my_watched_episodes'],
        my_start_date=anime_rec['my_start_date'],
        my_finish_date=anime_rec['my_finish_date'],
        my_score=anime_rec['my_score'],
        my_status=anime_rec['my_status'],
        my_rewatching=anime_rec['my_rewatching'],
        my_rewatching_ep=anime_rec['my_rewatching_ep'],
        my_last_updated=anime_rec['my_last_updated'],
        my_tags=anime_rec['my_tags'],
    )
    return anime_object


def anime_record_to_dict(anime_rec):
    anime_object = {
        'series_animedb_id': anime_rec['series_animedb_id'],  # this is MAL anime ID, enough to identify it
        'my_watched_episodes': anime_rec['my_watched_episodes'],
        'my_start_date': anime_rec['my_start_date'],
        'my_finish_date': anime_rec['my_finish_date'],
        'my_score': anime_rec['my_score'],
        'my_status': anime_rec['my_status'],
        'my_rewatching': anime_rec['my_rewatching'],
        'my_rewatching_ep': anime_rec['my_rewatching_ep'],
        'my_last_updated': anime_rec['my_last_updated'],
        'my_tags': anime_rec['my_tags'],
    }
    return anime_object


def load_users_pickle():
    with open(dataFile, 'rb') as f:
        users = pickle.load(f)
    return users.values()


def load_users_mongo(mongo, filter):
    users_db = mongo.mal.users
    return users_db.find(filter=filter).batch_size(50)   # trying smaller batch size so we don't get cursor timeout. Batch size should be small enough to be processed as whole in 10 minutes


def save_users_pickle(users):
    with open(dataFile, 'wb') as f:
        pickle.dump(users, f)


def save_users_mongo_ratings(mongo, users):
    if len(users) == 0:
        return
    operations = [pymongo.operations.UpdateOne(
        filter={"_id": user["_id"]},
        # I know what I want to update and my fields are non-overlapping, no overwrites, nice
        update={'$set': {
            'loadedRatings': user['loadedRatings'],
            'myinfo': user['myinfo'],
            'anime': user['anime'],
        }}
    ) for user in users]
    mongo.mal.users.bulk_write(operations)


def save_users_mongo_infos(mongo, users):
    # print('there is {} users with ids: {}'.format(len(users), [u['_id'] for u in users]))
    if len(users) == 0:
        return
    operations = [pymongo.operations.UpdateOne(
        filter={"_id": user["_id"]},
        # I know what I want to update and my fields are non-overlapping, no overwrites, nice
        update={'$set': {
            'loadedInfo': user['loadedInfo'],
            'info': user['info'],
        }}
    ) for user in users]
    mongo.mal.users.bulk_write(operations)


def load_user_data(username):
    apiUrl = 'https://kuristina.herokuapp.com/anime/' + username + '.json'  # base url
    print('Reading {} AnimeList from {}'.format(username, apiUrl))  # console message

    # API call to get JSON
    page = requests.get(apiUrl)
    if page.status_code == 503:  # I don't know why, but e.g. https://kuristina.herokuapp.com/anime/purplepinapples.json returns 503 and shuts down the app
        print('something is broken, fuck')
        return None

    c = page.content
    # Decoding JSON
    jsonData = json.loads(c)

    if jsonData['myanimelist'] is None:
        return None

    # checking keys
    if 'myinfo' not in jsonData['myanimelist']:
        return None

    return jsonData


if __name__ == '__main__':
    count = 0  # keep count of user for current session
    dataFile = 'UserList.rick'
    mongo = MongoClient('localhost', 27017)

    changed_users = []  # for mongo
    # users = load_users_pickle()
    users = load_users_mongo(mongo, {'loadedRatings': False})
    for user in users:
        username = user['username']

        if user['loadedRatings']:
            print('already loaded, skipping')
            continue

        apiUrl = 'https://kuristina.herokuapp.com/anime/' + username + '.json'  # base url
        print('Reading {} AnimeList from {}'.format(username, apiUrl))  # console message

        tries = 0
        jsonData = load_user_data(username)
        while tries < 3 and jsonData is None:
            tries += 1
            jsonData = load_user_data(username)

        if jsonData is None:
            continue

        # checking if json data is present
        if jsonData['myanimelist'] is not None:
            count += 1

            userData = jsonData['myanimelist']
            user['myinfo'] = userData['myinfo']
            if 'anime' in userData:
                # although I could persist all of data, half of every rating is info about anime, which should be kept with anime and not with every rating
                # so here I just whiteList everything I want
                user['anime'] = []

                # this is just mess coming from xml to json conversion, if there is only 1 anime, it is directly dict, not 1item list
                if type(userData['anime']) is dict:
                    userData['anime'] = [userData['anime']]

                for anime in userData['anime']:
                    # anime_record = anime_record_to_named_tuple(anime)  # named tuple for for pickle
                    anime_record = anime_record_to_dict(anime)  # classic dict for mongo
                    user['anime'].append(anime_record)
            else:
                user['anime'] = None    # just no data downloaded
            user['loadedRatings'] = True

            # for mongo
            changed_users.append(user)

            print('Writing data for {}-th user, {} complete.'.format(count, username))  # console message
        else:
            print(username, 'don\'t have any anime in their list.')
            # console message for those user who don't have any anime in their list

        # just dumping every 500 runs, the rate is about 1000 per hour, so this makes it flush cca each 30 minutes
        # flushing takes ca 4 minutes for 5 GB
        # every 100 for mongo, because I can
        if count % 100 == 0:
            print('{} users processed, persisting them'.format(count))
            # save_users_pickle(users)
            save_users_mongo_ratings(mongo, changed_users)
            print('dumping done')
            changed_users = []

    print('all users processed, persisting them')
    # save_users_pickle(users)
    save_users_mongo_ratings(mongo, changed_users)
    print('dumping done')

    print('Total', count, 'user data fetched. Done.')
