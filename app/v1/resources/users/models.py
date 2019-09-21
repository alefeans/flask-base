import json
from app import mongo
from bson.json_util import dumps


class Users:

    def __init__(self):
        pass

    @classmethod
    def get_all_users(cls):
        return json.loads(dumps(mongo.db.users.find().sort([('name', 1)])))

    @classmethod
    def get_user(cls, user):
        user = mongo.db.users.find_one({'username': user})
        if user:
            return json.loads(dumps(user))
        return None
