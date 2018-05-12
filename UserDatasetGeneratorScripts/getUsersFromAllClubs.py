import os
from createUserListFromClub import create_user_list_from_club

if __name__ == '__main__':
    # setting name of output file
    outputPath = 'user-lists/UserListClub{}.txt'

    for clubId in range(0, 100000):
        clubId = str(clubId)
        print('going to download for clubId: {}'.format(clubId))
        outputFile = outputPath.format(clubId)
        if os.path.exists(outputFile):
            continue

        create_user_list_from_club(clubId, outputFile)