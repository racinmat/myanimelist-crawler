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
    mongo = MongoClient('localhost', 27017)
    users_db = mongo.mal.users

    widgets = [progressbar.Percentage(), ' ', progressbar.Counter(), ' ', progressbar.Bar(), ' ',
               progressbar.FileTransferSpeed()]
    pbar = progressbar.ProgressBar(widgets=widgets, max_value=users_db.count()).start()
    counter = 0

    with open('UserList2.csv', 'w', newline='') as userFile:
        userWriter = csv.writer(userFile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        with open('UserAnimeList2.csv', 'w', newline='') as listFile:
            listWriter = csv.writer(listFile, delimiter=',',
                                    quotechar='"', quoting=csv.QUOTE_MINIMAL)

            # header
            userWriter.writerow(
                ['username', 'user_id', 'user_watching', 'user_completed', 'user_onhold', 'user_dropped',
                 'user_plantowatch', 'user_days_spent_watching', 'gender', 'location', 'birth_date',
                 'access_rank', 'join_date', 'last_online', 'stats_mean_score', 'stats_rewatched',
                 'stats_episodes'])

            # header
            listWriter.writerow(['username', 'anime_id', 'my_watched_episodes', 'my_start_date', 'my_finish_date',
                                 'my_score', 'my_status', 'my_rewatching', 'my_rewatching_ep', 'my_last_updated',
                                 'my_tags'])

            for user in users_db.find():
                counter += 1
                pbar.update(counter)

                if user['loadedRatings']:

                    rowData = [
                        user['username'],
                        user['myinfo']['user_id'],
                        user['myinfo']['user_watching'],
                        user['myinfo']['user_completed'],
                        user['myinfo']['user_onhold'],
                        user['myinfo']['user_dropped'],
                        user['myinfo']['user_plantowatch'],
                        user['myinfo']['user_days_spent_watching'],
                    ]
                    if user['loadedInfo']:
                        rowData.extend([
                            user['info']['gender'],
                            user['info']['location'],
                            user['info']['birth_date'],
                            user['info']['access_rank'],
                            user['info']['join_date'],
                            user['info']['last_online'],
                            user['info']['stats_mean_score'],
                            user['info']['stats_rewatched'],
                            user['info']['stats_episodes'],
                        ])
                    else:
                        rowData.extend([
                            '', '', '', '', '', '', '', '', ''
                        ])
                    userWriter.writerow(rowData)

                    if user['anime'] is None:
                        continue

                    # named tuple is used for anime
                    for anime in user['anime']:
                        listWriter.writerow([
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
