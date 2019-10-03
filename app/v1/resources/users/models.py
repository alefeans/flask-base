import json
from app import mongo
from flask_restplus import abort
from bson.json_util import dumps
from bson.objectid import ObjectId
from app.helpers import encrypt_password


class Users:

    def __init__(self):
        pass

    @staticmethod
    def get_all_users():
        return json.loads(dumps(mongo.db.users.find().sort([('username', 1)])))

    @staticmethod
    def get_user(id):
        user = mongo.db.users.find_one({'_id': ObjectId(id)})
        if user:
            return json.loads(dumps(user))
        return None

    @staticmethod
    def insert_user(user):
        if mongo.db.users.find_one({'username': user.get('username')}):
            abort(409, 'User already exists')

        user['password'] = encrypt_password(user.get('password', 'changeme'))
        if not mongo.db.users.insert_one(user).inserted_id:
            abort(422, 'Cannot create user')
        return json.loads(dumps(user))

    @classmethod
    def update_user(cls, id, data):
        if not cls.get_user(id):
            abort(404, 'User not found')

        if mongo.db.users.update_one({'_id': ObjectId(id)}, {'$set': data}):
            return '', 204
        abort(422, 'No user updated')

    @classmethod
    def delete_user(cls, id):
        if mongo.db.users.delete_one({'_id': ObjectId(id)}).deleted_count:
            return '', 204
        abort(404, 'User not found')
