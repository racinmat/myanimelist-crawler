'''
This script can be used to create user list from [**Myanimelist**](https://myanimelist.net/) using any forum post.
The idea is to extract user fro the post.

Output file contains list of username, one at each line.
'''
import json
import pickle
import time

if __name__ == '__main__':
    with open('UserList.rick', 'rb') as f:
        users = pickle.load(f)

    print('animelist data')
    print('{} unique users'.format(len(users)))
    print('{} of them have annotations'.format(len([u for u in users if users[u]['loadedRatings']])))
    print('{} anime records in total'.format(len([r for u in users if users[u]['loadedRatings'] and users[u]['anime'] is not None for r in users[u]['anime']])))
    print('{} score ratings for anime'.format(len([r for u in users if users[u]['loadedRatings'] and users[u]['anime'] is not None for r in users[u]['anime'] if r['my_score'] != '0'])))
    print('{} unique animes'.format(len(set([r['series_animedb_id'] for u in users if users[u]['loadedRatings'] and users[u]['anime'] is not None for r in users[u]['anime']]))))

    with open('UserInfo.rick', 'rb') as f:
        users = pickle.load(f)

    print('info data')
    print('{} unique users'.format(len(users)))
    print('{} of them have annotations'.format(len([u for u in users if users[u]['loadedInfo']])))
