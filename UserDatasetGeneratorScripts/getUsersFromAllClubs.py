import os
from createUserListFromClub import create_user_list_from_club

if __name__ == '__main__':
    # setting name of output file
    outputPath = 'user-lists/UserListClub{}.txt'

    # todo: check crawled data, some clubs have only first page crawled (=36 records in its file) even if there is more of them
    # there is 75855 clubs, 75855 is the last club ID as of 13.5.2018
    for clubId in range(0, 100000):
        clubId = str(clubId)
        print('going to download for clubId: {}'.format(clubId))
        outputFile = outputPath.format(clubId)
        if os.path.exists(outputFile):
            continue

        create_user_list_from_club(clubId, outputFile)