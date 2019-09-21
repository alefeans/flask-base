from flask_restplus import Resource, Namespace
from flask_jwt_extended import jwt_required
from .serializers import user
from .models import Users

api = Namespace('users', 'Users Endpoint')


@api.route('/')
class UserList(Resource):

    @api.marshal_list_with(user)
    @jwt_required
    def get(self):
        """
        Get all Users
        """
        return Users.get_all_users()


@api.param('user', 'The Username')
@api.route('/<string:user>')
class User(Resource):

    @api.marshal_with(user)
    @api.response(404, 'User not found')
    @jwt_required
    def get(self, user):
        """
        Get user by Username
        """
        user = Users.get_user(user)

        if not user:
            api.abort(404, 'User not found')
        return user
