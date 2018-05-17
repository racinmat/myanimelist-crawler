'''
This script can be used to create user list from [**Myanimelist**](https://myanimelist.net/) using any forum post.
The idea is to extract user fro the post.

Output file contains list of username, one at each line.
'''
import json
import pickle
import time
import csv
from utils import AnimeRecord
import progressbar

if __name__ == '__main__':
    mongo = MongoClient('localhost', 27017)
    users_db = mongo.mal.users

    with open('UserListBackup.rick', 'rb') as f:    # could take long, like this it wont interfere with the ongoing scraping
        users = pickle.load(f)

    with open('UserInfoBackup.rick', 'rb') as f:    # could take long, like this it wont interfere with the ongoing scraping
        usersInfo = pickle.load(f)

    print('data loaded, going to dump')

    widgets = [progressbar.Percentage(), ' ', progressbar.Counter(), ' ', progressbar.Bar(), ' ',
               progressbar.FileTransferSpeed()]
    pbar = progressbar.ProgressBar(widgets=widgets, max_value=len(users)).start()
    counter = 0

    with open('UserList.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # header
        writer.writerow(['username', 'user_id', 'user_watching', 'user_completed', 'user_onhold', 'user_dropped',
                         'user_plantowatch', 'user_days_spent_watching', 'gender', 'location', 'birth_date',
                         'access_rank', 'join_date', 'last_online', 'stats_mean_score', 'stats_rewatched',
                         'stats_episodes'])

        for username in users:
            counter += 1
            pbar.update(counter)

            user = users[username]
            userInfo = usersInfo[username]
            if not user['loadedRatings']:
                continue

            rowData = [
                username,
                user['myinfo']['user_id'],
                user['myinfo']['user_watching'],
                user['myinfo']['user_completed'],
                user['myinfo']['user_onhold'],
                user['myinfo']['user_dropped'],
                user['myinfo']['user_plantowatch'],
                user['myinfo']['user_days_spent_watching'],
            ]
            if userInfo['loadedInfo']:
                rowData.extend([
                    userInfo['info']['gender'],
                    userInfo['info']['location'],
                    userInfo['info']['birth_date'],
                    userInfo['info']['access_rank'],
                    userInfo['info']['join_date'],
                    userInfo['info']['last_online'],
                    userInfo['info']['stats_mean_score'],
                    userInfo['info']['stats_rewatched'],
                    userInfo['info']['stats_episodes'],
                ])
            else:
                rowData.extend([
                    '', '', '', '', '', '', '', '', ''
                ])
            writer.writerow(rowData)

    print('users dumped to csv, going to dump animelists')
    pbar = progressbar.ProgressBar(widgets=widgets, max_value=len(users)).start()
    counter = 0

    with open('UserAnimeList.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # header
        writer.writerow(['username', 'anime_id', 'my_watched_episodes', 'my_start_date', 'my_finish_date',
                         'my_score', 'my_status', 'my_rewatching', 'my_rewatching_ep', 'my_last_updated', 'my_tags'])

        for username in users:
            counter += 1
            pbar.update(counter)

            user = users[username]
            if not user['loadedRatings']:
                continue

            if user['anime'] is None:
                continue

            # named tuple is used for anime
            for anime in user['anime']:
                writer.writerow([
                    user['username'],
                    anime.series_animedb_id,
                    anime.my_watched_episodes,
                    anime.my_start_date,
                    anime.my_finish_date,
                    anime.my_score,
                    anime.my_status,
                    anime.my_rewatching,
                    anime.my_rewatching_ep,
                    anime.my_last_updated,
                    anime.my_tags,
                ])

    print('animelists dumped to csv')
