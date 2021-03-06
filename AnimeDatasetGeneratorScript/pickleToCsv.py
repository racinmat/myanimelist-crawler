'''
This script can be used to create user list from [**Myanimelist**](https://myanimelist.net/) using any forum post.
The idea is to extract user fro the post.

Output file contains list of username, one at each line.
'''
import json
import pickle
import time
import csv

import progressbar

if __name__ == '__main__':
    print('opening data')
    with open('AnimeList.rick', 'rb') as f:
        animes = pickle.load(f)
    print('data loaded, going to dump')

    widgets = [progressbar.Percentage(), ' ', progressbar.Counter(), ' ', progressbar.Bar(), ' ',
               progressbar.FileTransferSpeed()]
    pbar = progressbar.ProgressBar(widgets=widgets, max_value=len(animes)).start()
    counter = 0

    with open('AnimeList.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # header
        writer.writerow(['anime_id', 'title', 'title_english', 'title_japanese', 'title_synonyms', 'image_url', 'type',
                         'source', 'episodes', 'status', 'airing', 'aired_string', 'aired', 'duration', 'rating',
                         'score', 'scored_by', 'rank', 'popularity', 'members', 'favorites', 'background', 'premiered',
                         'broadcast', 'related', 'producer', 'licensor', 'studio', 'genre', 'opening_theme',
                         'ending_theme'])

        for id in animes:
            counter += 1
            pbar.update(counter)

            anime = animes[id]
            if not anime['loadedInfo']:
                continue
            writer.writerow([
                id,
                anime['title'],
                anime['title_english'],
                anime['title_japanese'],
                anime['title_synonyms'],
                anime['image_url'],
                anime['type'],
                anime['source'],
                anime['episodes'],
                anime['status'],
                anime['airing'],
                anime['aired_string'],
                anime['aired'],
                anime['duration'],
                anime['rating'],
                anime['score'],
                anime['scored_by'],
                anime['rank'],
                anime['popularity'],
                anime['members'],
                anime['favorites'],
                anime['background'],
                anime['premiered'],
                anime['broadcast'],
                anime['related'],
                ', '.join([i['name'] for i in anime['producer']]),
                ', '.join([i['name'] for i in anime['licensor']]),
                ', '.join([i['name'] for i in anime['studio']]),
                ', '.join([i['name'] for i in anime['genre']]),
                anime['opening_theme'],
                anime['ending_theme'],
            ])

    print('anime dumped to csv')
