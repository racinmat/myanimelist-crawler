'''
This script can be used to create user list from [**Myanimelist**](https://myanimelist.net/) using any forum post.
The idea is to extract user fro the post.

Output file contains list of username, one at each line.
'''
import json
import pickle
import time
from datetime import datetime

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt


def calculate_annotations(users_file, users_info_file):
    with open(users_file, 'rb') as f:
        users = pickle.load(f)

    with open(users_info_file, 'rb') as f:
        usersInfo = pickle.load(f)

    processed_ratings = [i for i, u in enumerate(users.keys()) if users[u]['loadedRatings']]
    processed_infos = [i for i, u in enumerate(usersInfo.keys()) if usersInfo[u]['loadedInfo']]

    plt.figure(figsize=(80, 6))
    plt.hist(processed_ratings, bins=30000, alpha=0.5, color='b', label='ratings')
    plt.hist(processed_infos, bins=30000, alpha=0.5, color='r', label='infos')
    plt.legend(loc='upper right')
    plt.savefig('processed_hist_{}.png'.format(datetime.now()))


if __name__ == '__main__':
    calculate_annotations('UserListBackup.rick', 'UserInfoBackup.rick')
