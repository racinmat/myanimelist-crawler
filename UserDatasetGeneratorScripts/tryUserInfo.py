'''
This script gathers users demographics data using the python-mal library.
So it can run in parallel with getUser.py, which rewrites the UserList.rick file, this uses separate file, UserData.rick
it will be later merged into UserList.py, but till that time, they will run in parallel

'''

# importing libraries
import myanimelist.session

session = myanimelist.session.Session()

if __name__ == '__main__':
    # here I just try the api and what could be useful
    username = 'RedvelvetDaisuki'
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
        'birth_date': userData.birthday,
        # 'about': userData.about,
        'access_rank': userData.access_rank,
        # 'clubs': userData.clubs,
        # 'friends': userData.friends,
        'join_date': userData.join_date,
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
