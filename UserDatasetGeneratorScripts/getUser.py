'''
This script can be used to download user dataset from [**Myanimelist**](https://myanimelist.net/) using an API, [**Kuristina**](https://github.com/TimboKZ/kuristina).

For CSV output, please use the pickleToCsv script.
'''

# importing libraries
import pickle
import requests
import json
import sys
from utils import AnimeRecord

count = 0  # keep count of user for current session

dataFile = 'UserList.rick'

with open(dataFile, 'rb') as f:
    users = pickle.load(f)

for username in users:
    user = users[username]

    if user['loadedRatings']:
        print('already loaded, skipping')
        continue

    apiUrl = 'https://kuristina.herokuapp.com/anime/' + username + '.json'  # base url
    print('Reading {} AnimeList from {}'.format(username, apiUrl))  # console message

    # API call to get JSON
    page = requests.get(apiUrl)
    if page.status_code == 503:     # I don't know why, but e.g. https://kuristina.herokuapp.com/anime/purplepinapples.json returns 503 and shuts down the app
        print('something is broken, fuck')
        continue

    c = page.content

    # Decoding JSON
    jsonData = json.loads(c)

    # checking if json data is present
    if jsonData['myanimelist'] is not None:
        count += 1

        userData = jsonData['myanimelist']
        user['myinfo'] = userData['myinfo']
        if 'anime' in userData:
            # although I could persist all of data, half of every rating is info about anime, which should be kept with anime and not with every rating
            # so here I just whiteList everything I want
            user['anime'] = []

            # this is just mess coming from xml to json conversion, if there is only 1 anime, it is directly dict, not 1item list
            if type(userData['anime']) is dict:
                userData['anime'] = [userData['anime']]

            for anime in userData['anime']:
                anime_record = AnimeRecord(
                    series_animedb_id=anime['series_animedb_id'],    # this is MAL anime ID, enough to identify it
                    my_watched_episodes=anime['my_watched_episodes'],
                    my_start_date=anime['my_start_date'],
                    my_finish_date=anime['my_finish_date'],
                    my_score=anime['my_score'],
                    my_status=anime['my_status'],
                    my_rewatching=anime['my_rewatching'],
                    my_rewatching_ep=anime['my_rewatching_ep'],
                    my_last_updated=anime['my_last_updated'],
                    my_tags=anime['my_tags'],
                )
                user['anime'].append(anime_record)
        else:
            user['anime'] = None    # just no data downloaded
        user['loadedRatings'] = True

        print('Writing data for {}-th user, {} complete.'.format(count, username))  # console message
    else:
        print(username, 'don\'t have any anime in their list.')
        # console message for those user who don't have any anime in their list

    # just dumping every 500 runs, the rate is about 1000 per hour, so this makes it flush cca each 30 minutes
    # flushing takes ca 4 minutes for 5 GB
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
