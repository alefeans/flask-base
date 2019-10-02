import json
from app import mongo
from bson.json_util import dumps


class Users:

    def __init__(self):
        pass

    @staticmethod
    def get_all_users():
        return json.loads(dumps(mongo.db.users.find().sort([('username', 1)])))

    @staticmethod
    def get_user(user):
        user = mongo.db.users.find_one({'username': user})
        if user:
            return json.loads(dumps(user))
        return None
