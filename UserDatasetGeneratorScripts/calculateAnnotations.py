'''
This script can be used to create user list from [**Myanimelist**](https://myanimelist.net/) using any forum post.
The idea is to extract user fro the post.

Output file contains list of username, one at each line.
'''
import json
import pickle
import time

if __name__ == '__main__':
    # start = time.time()
    # this is old, dont use it. And loading is 2 time faster in pickle than in json
    # with open('UserList.json', 'r') as f:
    #     users = json.load(f)
    with open('UserList.rick', 'rb') as f:
        users = pickle.load(f)

    # print('load time: {}'.format(time.time() - start))

    print('{} unique users'.format(len(users)))
    print('{} of them have annotations'.format(len([u for u in users if users[u]['loadedRatings']])))
    print('{} anime records in total'.format(len([r for u in users if users[u]['loadedRatings'] and users[u]['anime'] is not None for r in users[u]['anime']])))
    print('{} score ratings for anime'.format(len([r for u in users if users[u]['loadedRatings'] and users[u]['anime'] is not None for r in users[u]['anime'] if r['my_score'] != '0'])))
    print('{} unique animes'.format(len(set([r['series_animedb_id'] for u in users if users[u]['loadedRatings'] and users[u]['anime'] is not None for r in users[u]['anime']]))))
