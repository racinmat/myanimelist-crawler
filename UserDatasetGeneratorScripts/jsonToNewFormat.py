'''
This script can be used to create user list from [**Myanimelist**](https://myanimelist.net/) using any forum post.
The idea is to extract user fro the post.

Output file contains list of username, one at each line.
'''
import json
import pickle

if __name__ == '__main__':
    with open('UserList.json', 'r') as f:
        users = json.load(f)

    for username in users:
        user = users[username]
        if not user['loadedRatings']:
            continue
        if user['anime'] is None:
            continue
        user['anime_new'] = []

        # this is just mess coming from xml to json conversion, if there is only 1 anime, it is directly dict, not 1item list
        # only in old format, in the new one it will be ok
        if type(user['anime']) is dict:
            user['anime'] = [user['anime']]

        # print(type(user['anime']))
        for anime in user['anime']:
            if type(anime) is str:
                print(anime)
                print(user['anime'])
                print(user['username'])
            anime_record = {
                'series_animedb_id': anime['series_animedb_id'],  # this is MAL anime ID, enough to identify it
                'my_watched_episodes': anime['my_watched_episodes'],
                'my_start_date': anime['my_start_date'],
                'my_finish_date': anime['my_finish_date'],
                'my_score': anime['my_score'],
                'my_status': anime['my_status'],
                'my_rewatching': anime['my_rewatching'],
                'my_rewatching_ep': anime['my_rewatching_ep'],
                'my_last_updated': anime['my_last_updated'],
                'my_tags': anime['my_tags'],
            }
            user['anime_new'].append(anime_record)
        user['anime'] = user['anime_new']
        del user['anime_new']

    with open('UserList.json', 'w+') as f:
        json.dump(users, f)
