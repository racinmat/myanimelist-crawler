'''
This script can be used to create user list from [**Myanimelist**](https://myanimelist.net/) using any forum post.
The idea is to extract user fro the post.

Output file contains list of username, one at each line.
'''
import json
import pickle
import time


def calculate_annotations(users_file, users_info_file):
    with open(users_file, 'rb') as f:
        users = pickle.load(f)

    print('animelist data')
    print('{} unique users'.format(len(users)))
    print('{} of them have annotations'.format(len([u for u in users if users[u]['loadedRatings']])))
    print('{} anime records in total'.format(len([r for u in users if users[u]['loadedRatings'] and users[u]['anime'] is not None for r in users[u]['anime']])))
    print('{} score ratings for anime'.format(len([r for u in users if users[u]['loadedRatings'] and users[u]['anime'] is not None for r in users[u]['anime'] if r.my_score != '0'])))
    print('{} unique animes'.format(len(set([r.series_animedb_id for u in users if users[u]['loadedRatings'] and users[u]['anime'] is not None for r in users[u]['anime']]))))

    with open(users_info_file, 'rb') as f:
        usersInfo = pickle.load(f)

    print('info data')
    print('{} unique users'.format(len(usersInfo)))
    print('{} of them have annotations'.format(len([u for u in usersInfo if usersInfo[u]['loadedInfo']])))

    print('merged data')
    print('{} of them have all annotations'.format(len([u for u in usersInfo if users[u]['loadedRatings'] and usersInfo[u]['loadedInfo']])))
    print('{} of them have all annotations and some anime in animelist'.format(len([u for u in usersInfo if users[u]['loadedRatings'] and users[u]['anime'] is not None and usersInfo[u]['loadedInfo']])))


if __name__ == '__main__':
    calculate_annotations('UserList.rick', 'UserInfo.rick')
