'''
This script gathers users demographics data using the python-mal library.
So it can run in parallel with getUser.py, which rewrites the UserList.rick file, this uses separate file, UserData.rick
it will be later merged into UserList.py, but till that time, they will run in parallel

'''

# importing libraries
import pickle
import requests
import json
import sys
import myanimelist.session

count = 0  # keep count of user for current session

dataFile = 'UserInfo.rick'
session = myanimelist.session.Session()

with open(dataFile, 'rb') as f:
    users = pickle.load(f)

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
    except Exception as e:
        # raise e   # for debugging parsing
        pass

    # just dumping every 500 runs, the rate is about 2000 per hour, so this makes it flush cca each 15 minutes
    if count % 500 == 0:
        print('{} users processed, dumping them to file'.format(count))
        with open(dataFile, 'wb') as f:
            pickle.dump(users, f)
        print('dumping done')

print('all users processed, dumping them to file')
with open(dataFile, 'wb') as f:
    pickle.dump(users, f)
print('dumping done')

print('Total', count, 'user data fetched. Done.')
