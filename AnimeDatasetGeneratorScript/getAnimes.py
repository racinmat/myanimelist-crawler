'''
This script can be used to download anime dataset from [**Myanimelist**](https://myanimelist.net/) using an unofficial MyAnimeList REST API, [**Jikan**](https://jikan.me/docs).
Column metadata:

animeID: id of anime as in anime url https://myanimelist.net/anime/ID
name: title of anime
premiered: premiered on. default format (season year) 
genre: list of genre
type: type of anime (example TV, Movie etc) 
episodes: number of episodes
studios: list of studio
source: source of anime (example original, manga, game etc) 
scored: score of anime
scoredBy: number of member scored the anime
members: number of member added anime to their list
'''

# importing libraries
import pickle
import re
import requests
import json
import csv
import sys


def producer_url_to_id(url):
    m = re.search('https://myanimelist.net/anime/producer/(\d+)/*', url)
    return m.group(0)


def genre_url_to_id(url):
    m = re.search('https://myanimelist.net/anime/genre/(\d+)/*', url)
    return m.group(0)


count = 0  # keep count of anime	for current session

dataFile = 'AnimeList.rick'

with open(dataFile, 'rb') as f:
    animes = pickle.load(f)

for anime_id in animes:
    anime = animes[anime_id]

    if anime['loadedInfo']:
        print('already loaded, skipping')
        continue

    apiUrl = 'http://api.jikan.moe/anime/' + str(anime_id)  # base url for API
    print('Reading {} anime details from {}'.format(anime_id, apiUrl))
    # note: for SSL use 'https://api.jikan.me/'. For more go here 'https://jikan.me/docs'

    # API call
    page = requests.get(apiUrl)

    # I will do 5 retries
    tries = 0
    while tries < 5 and page.status_code != 200:
        tries += 1
        page = requests.get(apiUrl)

    # if status code is 200 then write to file
    if page.status_code != 200:
        print('some shit happened, ending with code {}'.format(page.status_code))
        break

    c = page.content
    # Decoding JSON
    jsonData = json.loads(c)

    count += 1

    anime['loadedInfo'] = True
    anime['title'] = jsonData['title']
    anime['title_english'] = jsonData['title_english']
    anime['title_japanese'] = jsonData['title_japanese']
    anime['title_synonyms'] = jsonData['title_synonyms']
    anime['image_url'] = jsonData['image_url']
    anime['type'] = jsonData['type']
    anime['source'] = jsonData['source']
    anime['episodes'] = jsonData['episodes']
    anime['status'] = jsonData['status']
    anime['airing'] = jsonData['airing']
    anime['aired_string'] = jsonData['aired_string']
    anime['aired'] = jsonData['aired']
    anime['duration'] = jsonData['duration']
    anime['rating'] = jsonData['rating']
    anime['score'] = jsonData['score']
    anime['scored_by'] = jsonData['scored_by']
    anime['rank'] = jsonData['rank']
    anime['popularity'] = jsonData['popularity']
    anime['members'] = jsonData['members']
    anime['favorites'] = jsonData['favorites']
    anime['background'] = jsonData['background']
    anime['premiered'] = jsonData['premiered']
    anime['broadcast'] = jsonData['broadcast']
    anime['related'] = jsonData['related']
    anime['producer'] = [{'id': producer_url_to_id(p['url']), 'name': p['name']} for p in jsonData['producer']]
    anime['licensor'] = [{'id': producer_url_to_id(p['url']), 'name': p['name']} for p in jsonData['licensor']]
    anime['studio'] = [{'id': producer_url_to_id(p['url']), 'name': p['name']} for p in jsonData['studio']]
    anime['genre'] = [{'id': genre_url_to_id(p['url']), 'name': p['name']} for p in jsonData['genre']]
    anime['opening_theme'] = jsonData['opening_theme']
    anime['ending_theme'] = jsonData['ending_theme']

    # just dumping every 200 runs
    if count % 200 == 0:
        print('{} animes processed, dumping them to file'.format(count))
        with open(dataFile, 'wb') as f:
            pickle.dump(animes, f)
        print('dumping done')

print('all users processed, dumping them to file')
with open(dataFile, 'wb') as f:
    pickle.dump(animes, f)
print('dumping done')

print('Total', count, 'anime data fetched. Done.')
