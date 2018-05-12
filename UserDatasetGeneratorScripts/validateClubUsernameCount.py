'''
This script can be used to create user list from [**Myanimelist**](https://myanimelist.net/) using any forum post.
The idea is to extract user fro the post.

Output file contains list of username, one at each line.
'''
import re
import time

from bs4 import BeautifulSoup
import requests
import sys
import glob

from createUserListFromClub import get_club_page

if __name__ == '__main__':
    usernames = set()

    for i, file in enumerate(glob.glob('user-lists/UserListClub*.txt')):
        m = re.search('UserListClub(\d+).txt', file)
        if m is None:
            continue
        clubID = m.group(0)
        with open(file, 'r') as f:
            loaded_names = f.read().split('\n')
        loaded_names = set([l for l in loaded_names if l])
        num_names = len(loaded_names)

        page = get_club_page(clubID, 0)

        if page.status_code != 200:
            continue

        c = page.content
        soup = BeautifulSoup(c, 'html.parser')  # parsing page

        # getting username in the page
        users = soup.find_all('td', 'borderClass')
        print(users.text)

        print('loaded {} names from file {}'.format(len(loaded_names), file))
        usernames = usernames.union(set(loaded_names))
        print('after file {}, there are {} unique names'.format(i, len(usernames)))

