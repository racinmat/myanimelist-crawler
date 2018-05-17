'''
This script can be used to create user list from [**Myanimelist**](https://myanimelist.net/) using any forum post.
The idea is to extract user fro the post.

Output file contains list of username, one at each line.
'''
import json
import pickle
import time


def fix_annotations(users_file, users_info_file):
    # sometimes loaded... is true, but no data is present fixing that
    with open(users_file, 'rb') as f:
        users = pickle.load(f)

    print('loaded data')
    wrong_count = 0

    for username in users:
        user = users[username]
        if user['loadedRatings'] and 'myinfo' not in user:
            wrong_count += 1
            user['loadedRatings'] = False

    print('{} wrong ratings annotations fixed for users, dumping it'.format(wrong_count))

    if wrong_count > 0:
        with open(users_file, 'wb') as f:
            pickle.dump(users, f)

    print('done users ratings, going for infos')

    with open(users_info_file, 'rb') as f:
        usersInfo = pickle.load(f)

    print('loaded data')
    wrong_count = 0

    for username in usersInfo:
        user = usersInfo[username]
        if user['loadedInfo'] and 'info' not in user:
            wrong_count += 1
            user['loadedInfo'] = False

    print('{} wrong info annotations fixed for users'.format(wrong_count))
    print('going to dump fixed data')

    with open(users_info_file, 'wb') as f:
        pickle.dump(usersInfo, f)


if __name__ == '__main__':
    fix_annotations('UserList.rick', 'UserInfo.rick')
