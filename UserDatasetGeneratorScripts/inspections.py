import pickle

if __name__ == '__main__':
    with open('UserListBackup.rick', 'rb') as f:
        users = pickle.load(f)

    with open('UserInfoBackup.rick', 'rb') as f:
        usersInfo = pickle.load(f)

    print('data loaded')
    withDataWithoutRatings = []
    for username in usersInfo:
        user = usersInfo[username]
        user2 = users[username]

        if not user['loadedInfo']:
            continue

        if user['loadedInfo'] and not user2['loadedRatings']:
            withDataWithoutRatings.append(username)
            print(username)

    print('{} users with info without ratings'.format(len(withDataWithoutRatings)))