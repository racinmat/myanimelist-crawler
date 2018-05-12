'''
This script can be used to create user list from [**Myanimelist**](https://myanimelist.net/) using any forum post.
The idea is to extract user fro the post.

Output file contains list of username, one at each line.
'''
import json
import pickle
import time

if __name__ == '__main__':
    with open('AnimeList.rick', 'rb') as f:
        animes = pickle.load(f)

    print('{} unique animes'.format(len(animes)))
    print('{} of them have annotations'.format(len([a for a in animes if animes[a]['loadedInfo']])))
