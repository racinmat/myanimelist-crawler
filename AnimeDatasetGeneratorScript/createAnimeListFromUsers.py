'''
This script only creates list of anime ids from users ratings so we have anime for all ratings and not any dangling foreign keys.
'''
import os
import pickle


with open('../UserDatasetGeneratorScripts/UserList.rick', 'rb') as f:
    users = pickle.load(f)

anime_ids = set()
pickleFile = 'AnimeList.rick'

for username in users:
    user = users[username]
    if not user['loadedRatings']:
        continue

    if user['anime'] is None:
        continue

    for anime in user['anime']:
        anime_ids.add(anime['series_animedb_id'])

print('{} unique animes written'.format(len(anime_ids)))
# this is for original getUser.py format
with open('AnimeList.txt', 'w+') as f:
    f.write('\n'.join(anime_ids))

# this is to keep users with other data, denormalized, perpared for multiple runs, for getUserJson
if os.path.exists(pickleFile):
    with open(pickleFile, 'rb') as f:
        animes = pickle.load(f)
else:
    animes = dict()

for anime_id in anime_ids:
    if anime_id in animes:
        continue
    animes[anime_id] = {'id': anime_id, 'loadedInfo': False}

with open(pickleFile, 'wb+') as f:
    pickle.dump(animes, f)
