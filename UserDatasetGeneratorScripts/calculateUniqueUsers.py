'''
This script can be used to create user list from [**Myanimelist**](https://myanimelist.net/) using any forum post.
The idea is to extract user fro the post.

Output file contains list of username, one at each line.
'''
import argparse
import os
import re
import time
import glob


def process_file(file):
    with open(file, 'r') as f:
        loaded_names = f.read().split('\n')
    loaded_names = set([l for l in loaded_names if l])
    return loaded_names


def process_usernames(usernames, loaded_names, old_len, id, i):
    usernames = usernames.union(set(loaded_names))
    if args.verbose or (i % 100 == 0):
        new_len = len(usernames)
        print('after file {}, there are {} unique names, {} additions'.format(id, new_len, new_len - old_len))
        old_len = new_len
    return usernames, old_len


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action='store_true')
    args = parser.parse_args()

    usernames = set()
    old_len = 0

    for i, file in enumerate(sorted(glob.glob('user-lists/UserListPost*.txt'), key=os.path.getmtime)):
        m = re.search('UserListPost(\d+).txt', file)
        if m is None:
            # print('fuck with {}'.format(file))
            threadID = 'unknown'
        else:
            threadID = m.group(0)

        loaded_names = process_file(file)
        usernames, old_len = process_usernames(usernames, loaded_names, old_len, threadID, i)

    for i, file in enumerate(sorted(glob.glob('user-lists/UserListClub*.txt'), key=os.path.getmtime)):
        m = re.search('UserListClub(\d+).txt', file)
        if m is None:
            # print('fuck with {}'.format(file))
            clubID = 'unknown'
        else:
            clubID = m.group(0)

        loaded_names = process_file(file)
        usernames, old_len = process_usernames(usernames, loaded_names, old_len, clubID, i)
