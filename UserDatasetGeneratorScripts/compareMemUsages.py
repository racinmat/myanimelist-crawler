'''
This script can be used to create user list from [**Myanimelist**](https://myanimelist.net/) using any forum post.
The idea is to extract user fro the post.

Output file contains list of username, one at each line.
'''
import json
import os
import pickle
import time
import csv
from collections import namedtuple
import progressbar
import psutil
from utils import AnimeRecord

def print_mem_usage():
    pid = os.getpid()
    py = psutil.Process(pid)
    mem_use = py.memory_info()[0]/2.**30    # memory usage in gb
    print('Current memory usage:', mem_use, 'GB')


if __name__ == '__main__':
    print_mem_usage()
    start = time.time()
    with open('UserListBackup.rick', 'rb') as f:
        users = pickle.load(f)

    print('time to load: ', time.time() - start)
    print_mem_usage()

    start = time.time()
    with open('UserListBackupTest.rick', 'wb+') as f:
        pickle.dump(users, f)
    print('time to save: ', time.time() - start)

    del users
    print_mem_usage()

    start = time.time()

    with open('UserListBackupTuple.rick', 'rb') as f:
        users = pickle.load(f)

    print('time to load: ', time.time() - start)
    print_mem_usage()

    start = time.time()
    with open('UserListBackupTupleTest.rick', 'wb+') as f:
        pickle.dump(users, f)
    print('time to save: ', time.time() - start)
