'''
This script can be used to create user list from [**Myanimelist**](https://myanimelist.net/) using any forum post.
The idea is to extract user fro the post.

Output file contains list of username, one at each line.
'''
import json
import pickle
import time
import csv
import pandas as pd

if __name__ == '__main__':
    animes = pd.read_csv('../AnimeDatasetGeneratorScript/AnimeList.csv')
    users = pd.read_csv('UserList.csv')
    animeLists = pd.read_csv('UserAnimeList.csv')

    print('everything loaded ok')