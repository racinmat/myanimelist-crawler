'''
Just calculates some fast stats, no using any complex queries
'''

import json
import pickle
import time

from pymongo import MongoClient


def calculate_annotations(users_file, users_info_file):
    mongo = MongoClient('localhost', 27017)
    users_db = mongo.mal.users

    print('{} unique users'.format(users_db.count()))
    print('{} of them have ratings annotations'.format(users_db.find({'loadedRatings': True}).count()))
    print('{} of them have info annotations'.format(users_db.find({'loadedInfo': True}).count()))
    print('{} of them have gender'.format(users_db.find({'loadedInfo': True, "info.gender": {"$ne": None}}).count()))
    print('{} of them have location'.format(users_db.find({'loadedInfo': True, "info.location": {"$ne": None}}).count()))
    print('{} of them have gender and location'.format(users_db.find({'loadedInfo': True, "info.gender": {"$ne": None}, "info.location": {"$ne": None}}).count()))
    print('{} of them have ratings and gender'.format(users_db.find({'loadedRatings': True, 'loadedInfo': True, "info.gender": {"$ne": None}}).count()))
    print('{} of them have all annotations'.format(users_db.find({'loadedRatings': True, 'loadedInfo': True}).count()))


if __name__ == '__main__':
    calculate_annotations('UserList.rick', 'UserInfo.rick')
