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
    # with open('UserListBackup.rick', 'rb') as f:    # could take long, like this it wont interfere with the ongoing scraping
    #     users = pickle.load(f)

    with open('UserInfoBackup.rick', 'rb') as f:    # could take long, like this it wont interfere with the ongoing scraping
        usersInfo = pickle.load(f)

    print('data loaded, going to merge')

    # for username in users:
    #     user = users[username]
    #     userInfo = usersInfo[username]
    #     if userInfo['loadedInfo']:
    #         user['loadedInfo'] = True
    #         user['info'] = userInfo['info']

    print('merged, going to fill db')

    mongo = MongoClient('localhost', 27017)
    users_db = mongo.mal.try_users

    # date without time is not supported https://stackoverflow.com/questions/30553406/python-bson-errors-invaliddocument-cannot-encode-object-datetime-date2015-3
    # converting it into datetime
    print('type(usersInfo)', type(usersInfo))
    for username in usersInfo:
        print('inserting', username)
        user = usersInfo[username]
        # here comes da mapping to datetime
        if user['loadedInfo']:
            if user['info']['join_date'] is not None:
                user['info']['join_date'] = datetime.datetime.combine(user['info']['join_date'], datetime.time())
            if user['info']['birth_date'] is not None:
                user['info']['birth_date'] = datetime.datetime.combine(user['info']['birth_date'], datetime.time())
        users_db.insert_one(user)
    users_db.insert_many(usersInfo)

    print('db filled')
