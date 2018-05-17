'''
This script can be used to create user list from [**Myanimelist**](https://myanimelist.net/) using any forum post.
The idea is to extract user fro the post.

Output file contains list of username, one at each line.
'''
import datetime
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
    widgets = [progressbar.Percentage(), ' ', progressbar.Counter(), ' ', progressbar.Bar(), ' ',
               progressbar.FileTransferSpeed()]
    pbar = progressbar.ProgressBar(widgets=widgets, max_value=len(users)).start()
    counter = 0

    for username in users:
        counter += 1
        pbar.update(counter)
        user = users[username]
        userInfo = usersInfo[username]
        if userInfo['loadedInfo']:
            user['loadedInfo'] = True
            user['info'] = userInfo['info']
            if user['info']['join_date'] is not None:
                user['info']['join_date'] = datetime.datetime.combine(user['info']['join_date'], datetime.time())
            if user['info']['birth_date'] is not None:
                user['info']['birth_date'] = datetime.datetime.combine(user['info']['birth_date'], datetime.time())

        # transforming from namedtuples to dicts
        if user['loadedRatings'] and user['anime'] is not None:
            user['anime'] = [anime._asdict() for anime in user['anime']]

    print('merged, going to fill db')

    mongo = MongoClient('localhost', 27017)
    users_db = mongo.mal.users

    pbar = progressbar.ProgressBar(widgets=widgets, max_value=len(users)).start()
    counter = 0

    for username in users:
        counter += 1
        pbar.update(counter)
        user = users[username]
        user['_id'] = username

        # from named tuple into dict
        users_db.insert_one(user)

    print('db filled')
