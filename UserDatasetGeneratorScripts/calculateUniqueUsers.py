'''
This script can be used to create user list from [**Myanimelist**](https://myanimelist.net/) using any forum post.
The idea is to extract user fro the post.

Output file contains list of username, one at each line.
'''
import os
import re
import time

from bs4 import BeautifulSoup
import requests
import sys
import glob

if __name__ == '__main__':
    usernames = set()

    for i, file in enumerate(sorted(glob.glob('user-lists/UserListPost*.txt'), key=os.path.getmtime)):
        m = re.search('UserListPost(\d+).txt', file)
        if m is None:
            # print('fuck with {}'.format(file))
            threadID = 'unknown'
        else:
            threadID = m.group(0)

        with open(file, 'r') as f:
            loaded_names = f.read().split('\n')
        loaded_names = set([l for l in loaded_names if l])
        # print('loaded {} names from file {}'.format(len(loaded_names), file))
        old_len = len(usernames)
        usernames = usernames.union(set(loaded_names))
        new_len = len(usernames)
        print('after file {}, there are {} unique names, {} additions'.format(threadID, new_len, new_len - old_len))

    for i, file in enumerate(sorted(glob.glob('user-lists/UserListClub*.txt'), key=os.path.getmtime)):
        m = re.search('UserListClub(\d+).txt', file)
        if m is None:
            # print('fuck with {}'.format(file))
            clubID = 'unknown'
        else:
            clubID = m.group(0)

        with open(file, 'r') as f:
            loaded_names = f.read().split('\n')
        loaded_names = set([l for l in loaded_names if l])
        # print('loaded {} names from file {}'.format(len(loaded_names), file))
        old_len = len(usernames)
        usernames = usernames.union(set(loaded_names))
        new_len = len(usernames)
        print('after file {}, there are {} unique names, {} additions'.format(clubID, new_len, new_len - old_len))
