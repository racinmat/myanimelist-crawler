'''
This script can be used to create user list from [**Myanimelist**](https://myanimelist.net/) using any forum post.
The idea is to extract user fro the post.

Output file contains list of username, one at each line.
'''
import os
import time
import urllib.request
from urllib.error import HTTPError

import requests
import sys
from joblib import Parallel, delayed
import progressbar

# setting name of output file
outputFile = 'ClubIds.txt'
outputLastFile = 'last_club_id.txt'

f = open(outputFile, 'a+')  # opening output file in write mode


def check_and_write(topicID):
    if 'pbar' in globals() and 'counter' in globals():
        global counter
        counter += 1
        pbar.update(counter)

    # if topicID % 1000 == 0:
    #     print('\nChecking topicID {}'.format(topicID))  # console message indicating number of comments

    topicID = str(topicID)
    url = 'https://myanimelist.net/clubs.php?cid=' + topicID
    page = requests.get(url)  # getting page
    while page.status_code == 429:  # too many requests
        time.sleep(1)
        page = requests.get(url)  # getting page
    if page.status_code != 200:
        print(topicID + ' has status code ' + str(page.status_code))
        return

    # try:
    #     page = urllib.request.urlopen(url)
    # except HTTPError:
    #     return

    print(topicID)
    f.write(topicID + '\n')
    f.flush()
    os.fsync(f)

widgets = [progressbar.Percentage(), ' ', progressbar.Counter(), ' ', progressbar.Bar(), ' ',
           progressbar.FileTransferSpeed()]


# check_and_write(0)

# pbar = progressbar.ProgressBar(widgets=widgets, max_value=1500000).start()
# counter = 0

# Parallel(n_jobs=20)(delayed(check_and_write)(i) for i in range(1500000))
last_id = 0
if os.path.exists(outputLastFile):
    with open(outputLastFile, 'r') as last_id_f:
        last_id = int(last_id_f.read(100))

for i in range(last_id, 100000):
    if i % 100 == 0:
        with open(outputLastFile, 'w+') as last_id_f:
            last_id_f.write(str(i))
    check_and_write(i)

f.close()  # closing file

print('Done writing username to output file.\nOutput:', outputFile)
