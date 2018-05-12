'''
This script can be used to create user list from [**Myanimelist**](https://myanimelist.net/) using any forum post.
The idea is to extract user fro the post.

Output file contains list of username, one at each line.
'''
import json
import pickle
import time

if __name__ == '__main__':
    with open('UserList.json', 'r') as f:
        users = json.load(f)

    start = time.time()

    with open('UserList.rick', 'wb+') as f:
        pickle.dump(users, f)

    print('save time pickle: {}'.format(time.time() - start))
    start = time.time()

    with open('UserList.json', 'w+') as f:
        json.dump(users, f)

    print('save time json: {}'.format(time.time() - start))
