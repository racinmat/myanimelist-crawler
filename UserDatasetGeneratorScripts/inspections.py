import pickle

from pymongo import MongoClient

if __name__ == '__main__':
    # with open('UserListBackup.rick', 'rb') as f:
    #     users = pickle.load(f)
    #
    # with open('UserInfoBackup.rick', 'rb') as f:
    #     usersInfo = pickle.load(f)
    #
    # print('data loaded')
    # withDataWithoutRatings = []
    # for username in usersInfo:
    #     user = usersInfo[username]
    #     user2 = users[username]
    #
    #     if not user['loadedInfo']:
    #         continue
    #
    #     if user['loadedInfo'] and not user2['loadedRatings']:
    #         withDataWithoutRatings.append(username)
    #         print(username)
    #
    # print('{} users with info without ratings'.format(len(withDataWithoutRatings)))

    mongo = MongoClient('localhost', 27017)
    users_db = mongo.mal.users

    # print('{} anime records in total'.format(users_db.aggregate({
    #     'project': {
    #         'loadedRatings': True,
    #         'anime': {"$ne": None},
    #         'total': {
    #             '$sum': {'$size': '$anime'}}
    #     }
    # })[0]))
    # print('{} anime records in total'.format(list(users_db.aggregate([
    #     # {'$limit': 5},
    #     {'$match':
    #         {'$and': [
    #             {'loadedRatings': {'$eq': True}},
    #             {'anime': {"$ne": None}}
    #         ]}
    #     },
    #     {'$project': {
    #         # "_id": {"$ifNull": ["$anime", []]},
    #         # 'item': 1,
    #         'list_size': {'$size': '$anime'}
    #     }},
    #     {'$group': {
    #         '_id': None,
    #         'total_size': {'$sum': "$list_size"},
    #     }}
    # ]))[0]['total_size']))

    # calculating all anime records
    # print('{} anime records in total'.format(list(users_db.aggregate([
    #     {'$match': {'$and': [{'loadedRatings': {'$eq': True}}, {'anime': {"$ne": None}}]}},
    #     {'$project': {'list_size': {'$size': '$anime'}}},
    #     {'$group': {'_id': None, 'total_size': {'$sum': "$list_size"}}}
    # ]))[0]['total_size']))

    print('{} anime records in total'.format(list(users_db.aggregate([
        {'$match': {'$and': [{'loadedRatings': {'$eq': True}}, {'anime': {"$ne": None}}]}},
        {'$unwind': {
            'path': '$anime',
            'preserveNullAndEmptyArrays': False
        }},
        # {'$project': {'list_size': {'$size': '$anime'}}},
        # {'$group': {'_id': None, 'total_size': {'$sum': "$anime"}}}
        {'$count': 'total_size'}
    ]))[0]['total_size']))

    # calculating only ratings

    print('{} anime records in total'.format(list(users_db.aggregate([
        {'$match': {'$and': [{'loadedRatings': {'$eq': True}}, {'anime': {"$ne": None}}]}},
        {'$unwind': {
            'path': '$anime',
            'preserveNullAndEmptyArrays': False
        }},
        {'$match': {'anime.my_score': {'$ne': '0'}}},
        # {'$project': {'list_size': {'$size': '$anime'}}},
        # {'$group': {'_id': None, 'total_size': {'$sum': "$anime"}}}
        {'$count': 'total_size'}
    ]))[0]['total_size']))
