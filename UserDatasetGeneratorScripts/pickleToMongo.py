'''
This script can be used to create user list from [**Myanimelist**](https://myanimelist.net/) using any forum post.
The idea is to extract user fro the post.

Output file contains list of username, one at each line.
'''
import json
import pickle
import time
import csv

from pymongo import MongoClient

from utils import AnimeRecord
import progressbar

if __name__ == '__main__':
    with open('UserListBackup.rick', 'rb') as f:    # could take long, like this it wont interfere with the ongoing scraping
        users = pickle.load(f)

    with open('UserInfoBackup.rick', 'rb') as f:    # could take long, like this it wont interfere with the ongoing scraping
        usersInfo = pickle.load(f)

    print('data loaded, going to merge')

    for username in users:
        user = users[username]
        userInfo = usersInfo[username]
        if usersInfo['loadedInfo']:
            user['loadedInfo'] = True
            user['info'] = userInfo['info']

    print('merged, going to fill db')

    mongo = MongoClient('localhost', 27017)
    users_db = mongo.mal.users

    users_db.insert_many(users)

    print('db filled')
