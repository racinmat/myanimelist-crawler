'''
This script can be used to create user list from [**Myanimelist**](https://myanimelist.net/) using any forum post.
The idea is to extract user fro the post.

Output file contains list of username, one at each line.
'''
import json
import pickle
import time
import csv
from collections import namedtuple

import progressbar

from utils import AnimeRecord

if __name__ == '__main__':

    with open('UserListBackup.rick', 'rb') as f:    # could take long, like this it wont interfere with the ongoing scraping
        users = pickle.load(f)

    print('data loaded')

    widgets = [progressbar.Percentage(), ' ', progressbar.Counter(), ' ', progressbar.Bar(), ' ',
               progressbar.FileTransferSpeed()]
    pbar = progressbar.ProgressBar(widgets=widgets, max_value=len(users)).start()
    counter = 0

    # creating namedtuple from dict for animelist records
    for username in users:
        counter += 1
        pbar.update(counter)

        user = users[username]
        if not user['loadedRatings']:
            continue

        if user['anime'] is None:
            continue

        user['anime'] = [AnimeRecord(**a) for a in user['anime']]

    with open('UserListBackupTuple.rick', 'wb') as f:
        pickle.dump(users, f)
