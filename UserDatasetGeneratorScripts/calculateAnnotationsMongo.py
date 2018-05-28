'''
This script can be used to create user list from [**Myanimelist**](https://myanimelist.net/) using any forum post.
The idea is to extract user fro the post.

Output file contains list of username, one at each line.
'''
import json
import pickle
import time

from pymongo import MongoClient


# should output during check:
# animelist data
# 302841 unique users
# 146700 of them have annotations
# 45626200 anime records in total
# 26832473 score ratings for anime
# 14441 unique animes
# 0 of them have annotations but not data
# info data
# 302841 unique users
# 131792 of them have annotations
# 0 of them have annotations but not info
# 95758 of them have gender
# 53452 of them have ratings and gender
# merged data
# 68975 of them have all annotations
# 66526 of them have all annotations and some anime in animelist

def calculate_annotations(users_file, users_info_file):
    mongo = MongoClient('localhost', 27017)
    users_db = mongo.mal.users

    print('users data')
    print('{} unique users'.format(users_db.count()))
    print('{} of them have ratings annotations'.format(users_db.find({'loadedRatings': True}).count()))
    print('{} anime records in total'.format(list(users_db.aggregate([
        {'$match': {'$and': [{'loadedRatings': {'$eq': True}}, {'anime': {"$ne": None}}]}},
        {'$unwind': {'path': '$anime', 'preserveNullAndEmptyArrays': False}},
        {'$count': 'total_size'}
    ]))[0]['total_size']))
    print('{} score ratings for anime'.format(list(users_db.aggregate([
        {'$match': {'$and': [{'loadedRatings': {'$eq': True}}, {'anime': {"$ne": None}}]}},
        {'$unwind': {'path': '$anime', 'preserveNullAndEmptyArrays': False}},
        {'$match': {'anime.my_score': {'$ne': '0'}}},
        {'$count': 'total_size'}
    ]))[0]['total_size']))
    print('{} unique animes'.format(list(users_db.aggregate([
        {'$match': {'$and': [{'loadedRatings': {'$eq': True}}, {'anime': {"$ne": None}}]}},
        {'$unwind': {'path': '$anime','preserveNullAndEmptyArrays': False}},
        {'$group': {'_id': '$anime.series_animedb_id', 'anime': {'$sum': 1}}},
        {'$count': 'anime'}
    ]))[0]['anime']))
    print('{} of them have annotations but not data'.format(users_db.find({'loadedRatings': True, "myinfo": {"$exists": False}}).count()))
    print('{} of them have info annotations'.format(users_db.find({'loadedInfo': True}).count()))
    print('{} of them have info annotations but not info'.format(users_db.find({'loadedInfo': True, "info": {"$exists": False}}).count()))
    print('{} of them have gender'.format(users_db.find({'loadedInfo': True, "info.gender": {"$ne": None}}).count()))
    print('{} of them have ratings and gender'.format(users_db.find({'loadedRatings': True, 'loadedInfo': True, "info.gender": {"$ne": None}}).count()))

    print('merged data')
    print('{} of them have all annotations'.format(users_db.find({'loadedRatings': True, 'loadedInfo': True}).count()))
    print('{} of them have all annotations and some anime in animelist'.format(users_db.find({'loadedRatings': True, 'loadedInfo': True, 'anime': {"$ne": None}}).count()))


if __name__ == '__main__':
    calculate_annotations('UserList.rick', 'UserInfo.rick')
# max club id 41128