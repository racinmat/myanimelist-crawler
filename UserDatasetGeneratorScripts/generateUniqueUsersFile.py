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
from bs4 import BeautifulSoup
import requests
import sys
import glob


def generate_unique_users(pickleFile):
    usernames = set()

    for i, file in enumerate(sorted(glob.glob('user-lists/*.txt'), key=os.path.getmtime)):
        with open(file, 'r') as f:
            loaded_names = f.read().split('\n')
        loaded_names = set([l for l in loaded_names if l])
        usernames = usernames.union(set(loaded_names))

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
