'''
This script gathers users demographics data using the python-mal library.
So it can run in parallel with getUser.py, which rewrites the UserList.rick file, this uses separate file, UserData.rick
it will be later merged into UserList.py, but till that time, they will run in parallel

'''

# importing libraries
import pickle

import pymongo
import requests
import json
import sys
import myanimelist.session
from pymongo import MongoClient
from getUser import *

if __name__ == '__main__':
    count = 0  # keep count of user for current session

    dataFile = 'UserInfo.rick'
    mongo = MongoClient('localhost', 27017)
    session = myanimelist.session.Session()

    changed_users = []  # for mongo
    # users = load_users_pickle()
    users = load_users_mongo()
    for username in users:
        user = users[username]

        if user['loadedInfo']:
            print('already loaded, skipping')
            continue

        print('going to dump data for username {}'.format(username))
        userData = session.user(username)

        try:
            userData.load()
            count += 1

            # from stats, I only want mean score, total entries, rewatched and episodes, the rest already is scraped with animelists
            user['loadedInfo'] = True
            user['info'] = {
                'gender': userData.gender,
                'location': userData.location,
                'birth_date': userData.birthday,
                'access_rank': userData.access_rank,
                'join_date': userData.join_date,
                'last_online': userData.last_online,
                'stats_mean_score': userData.anime_stats['Mean Score'],
                'stats_rewatched': userData.anime_stats['Rewatched'],
                'stats_episodes': userData.anime_stats['Episodes'],
            }

            # for mongo
            changed_users.append(user)
        except Exception as e:
            # raise e   # for debugging parsing
            pass

        # just dumping every 500 runs, the rate is about 2000 per hour, so this makes it flush cca each 15 minutes
        if count % 500 == 0:
            print('{} users processed, persisting them'.format(count))
            # save_users_pickle(users)
            save_users_mongo_infos(changed_users)
            print('dumping done')
            changed_users = []

    print('all users processed, persisting them')
    # save_users_pickle(users)
    save_users_mongo_infos(changed_users)
    print('dumping done')

    print('Total', count, 'user data fetched. Done.')
