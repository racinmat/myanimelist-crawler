'''
This script gathers users demographics data using the python-mal library.
So it can run in parallel with getUser.py, which rewrites the UserList.rick file, this uses separate file, UserData.rick
it will be later merged into UserList.py, but till that time, they will run in parallel

'''

# importing libraries
import datetime
import json

import requests

import myanimelist.session
from pymaybe import maybe

from utils import AnimeRecord

session = myanimelist.session.Session()


def load_user_info(username):
    userData = session.user(username)
    # print(userData)

    userData.load()
    # userData.load_clubs()
    # userData.load_friends()
    # userData.load_recommendations()
    # userData.load_reviews()

    info = {
        'gender': userData.gender,
        'location': userData.location,
        'birth_date': None if userData.birthday is None else datetime.datetime.combine(userData.birthday, datetime.time()),
        # 'about': userData.about,
        'access_rank': userData.access_rank,
        # 'clubs': userData.clubs,
        # 'friends': userData.friends,
        'join_date': None if userData.join_date is None else datetime.datetime.combine(userData.join_date, datetime.time()),
        'last_online': userData.last_online,
        # 'reviews': userData.reviews,
        # 'recommendations': userData.recommendations,
        # 'anime_list_views': userData.anime_list_views,
        'anime_stats': userData.anime_stats,    # from stats, I only want mean score, total entries, rewatched and episodes, the rest already is scraped with animelists
        'stats_mean_score': userData.anime_stats['Mean Score'],
        'stats_rewatched': userData.anime_stats['Rewatched'],
        'stats_episodes': userData.anime_stats['Episodes'],
        # 'anime_list': userData.anime_list(),
        # 'favorite_anime': userData.favorite_anime,
        # 'favorite_characters': userData.favorite_characters,
        # 'favorite_people': userData.favorite_people,
        # 'last_list_updates': userData.last_list_updates,
    }
    print(info)


def load_user_ratings(username):

    apiUrl = 'https://kuristina.herokuapp.com/anime/' + username + '.json'  # base url
    print('Reading {} AnimeList from {}'.format(username, apiUrl))  # console message

    # API call to get JSON
    page = requests.get(apiUrl)
    if page.status_code == 503:     # I don't know why, but e.g. https://kuristina.herokuapp.com/anime/purplepinapples.json returns 503 and shuts down the app
        print('something is broken, fuck')
        return

    c = page.content

    # Decoding JSON
    jsonData = json.loads(c)

    # checking if json data is present
    if jsonData['myanimelist'] is not None:
        userData = jsonData['myanimelist']
        info = userData['myinfo']
        if 'anime' in userData:
            # although I could persist all of data, half of every rating is info about anime, which should be kept with anime and not with every rating
            # so here I just whiteList everything I want
            animes = []

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
                animes.append(anime_record)
            print('animelist loaded')
        else:
            animes = None    # just no data downloaded
            print('adata loaded, but no animelist')


if __name__ == '__main__':
    # here I just try the api and what could be useful
    # username = 'RedvelvetDaisuki'
    # username = 'imagematerial'
    # username = 'shuzzable'
    # username = 'Kallykon'
    # username = 'Crispy_Steak'
    # username = 'Io_otonashi'
    username = 'abystoma2'
    load_user_info(username)
    # load_user_ratings(username)