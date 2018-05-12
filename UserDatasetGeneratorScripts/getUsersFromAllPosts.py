import os
from createUserListFromPost import create_user_list_from_post

if __name__ == '__main__':
    # setting name of output file
    outputPath = 'user-lists/UserListPost{}.txt'

    for threadId in range(0, 1500000):
        threadId = str(threadId)
        print('going to download for ThreadId: {}'.format(threadId))
        outputFile = outputPath.format(threadId)
        if os.path.exists(outputFile):
            continue

        create_user_list_from_post(threadId, outputFile)
