'''
This script can be used to create user list from [**Myanimelist**](https://myanimelist.net/) using any forum post.
The idea is to extract user fro the post.

Output file contains list of username, one at each line.
'''

import json
import os
import pickle
import re
import time

import progressbar
from bs4 import BeautifulSoup
import requests
import sys
import glob


def generate_unique_users(pickleFile):
    print('searching files')
    files = glob.glob('user-lists/*.txt')
    print('done searching, going to extract usernames from {} files'.format(len(files)))

    widgets = [progressbar.Percentage(), ' ', progressbar.Counter(), ' ', progressbar.Bar(), ' ',
               progressbar.FileTransferSpeed()]
    pbar = progressbar.ProgressBar(widgets=widgets, max_value=len(files)).start()

    # just appending lists inplace and creating the set afterwards is much faster than creating union per each file
    usernames = []

    for i, file in enumerate(files):
        pbar.update(i)

        with open(file, 'r') as f:
            loaded_names = f.read().split('\n')

        # data clansing per 2000 iterations, getting rid of duplicates once at a time makes it faster a lot
        if i % 2000 == 0:
            usernames = [l for l in usernames if l]  # to clear of empty strings
            usernames = list(set(usernames))

        usernames.extend(loaded_names)

    usernames = [l for l in usernames if l]  # to clear of empty strings
    usernames = set(usernames)

    print('{} unique usernames written'.format(len(usernames)))
    # this is for original getUser.py format
    with open('UserList.txt', 'w+') as f:
        f.write('\n'.join(usernames))

    # this is to keep users with other data, denormalized, perpared for multiple runs, for getUserJson
    if os.path.exists(pickleFile):
        with open(pickleFile, 'rb') as f:
            users = pickle.load(f)
    else:
        users = dict()

    for username in usernames:
        if username in users:
            continue
        users[username] = {'username': username, 'loadedRatings': False, 'loadedInfo': False}

    with open(pickleFile, 'wb+') as f:
        pickle.dump(users, f)


if __name__ == '__main__':
    pickleFile = 'UserList.rick'
    generate_unique_users(pickleFile)
