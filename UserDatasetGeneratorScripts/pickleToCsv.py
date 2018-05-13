'''
This script can be used to create user list from [**Myanimelist**](https://myanimelist.net/) using any forum post.
The idea is to extract user fro the post.

Output file contains list of username, one at each line.
'''
import json
import pickle
import time
import csv

if __name__ == '__main__':
    with open('UserListBackup.rick', 'rb') as f:    # could take long, like this it wont interfere with the ongoing scraping
        users = pickle.load(f)

    with open('UserList.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # header
        writer.writerow(['username', 'user_id', 'user_watching', 'user_completed', 'user_onhold', 'user_dropped',
                         'user_plantowatch', 'user_days_spent_watching'])

        for username in users:
            user = users[username]
            if not user['loadedRatings']:
                continue
            writer.writerow([username, user['myinfo']['user_id'], user['myinfo']['user_watching'],
                             user['myinfo']['user_completed'], user['myinfo']['user_onhold'],
                             user['myinfo']['user_dropped'], user['myinfo']['user_plantowatch'],
                             user['myinfo']['user_days_spent_watching']])

    print('users dumped to csv, going to dump animelists')

    with open('UserAnimeList.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # header
        writer.writerow(['username', 'anime_id', 'my_watched_episodes', 'my_start_date', 'my_finish_date',
                         'my_score', 'my_status', 'my_rewatching', 'my_rewatching_ep', 'my_last_updated', 'my_tags'])

        for username in users:
            user = users[username]
            if not user['loadedRatings']:
                continue

            if user['anime'] is None:
                continue

            for anime in user['anime']:
                writer.writerow([
                    user['username'],
                    anime['series_animedb_id'],
                    anime['my_watched_episodes'],
                    anime['my_start_date'],
                    anime['my_finish_date'],
                    anime['my_score'],
                    anime['my_status'],
                    anime['my_rewatching'],
                    anime['my_rewatching_ep'],
                    anime['my_last_updated'],
                    anime['my_tags'],
                ])

    print('animelists dumped to csv')
