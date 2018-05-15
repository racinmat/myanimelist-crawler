'''
This script can be used to create user list from [**Myanimelist**](https://myanimelist.net/) using any forum post.
The idea is to extract user fro the post.

Output file contains list of username, one at each line.
'''
import json
import pickle
import time

from calculateAnnotations import calculate_annotations

if __name__ == '__main__':
    calculate_annotations('UserListBackup.rick', 'UserInfoBackup.rick')
