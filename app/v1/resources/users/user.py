from flask_restplus import Resource, Namespace
from flask_jwt_extended import jwt_required
from .serializers import user, create_user
from .models import Users

api = Namespace('users', 'Users Endpoint')


@api.route('/')
class UserList(Resource):

    @api.marshal_list_with(user)
    @jwt_required
    def get(self):
        """
        Get all users
        """
        return Users.get_all_users()

    @api.marshal_with(user, code=201)
    @api.expect(create_user)
    @api.doc(responses={
        400: 'Input payload validation failed',
        401: 'Unauthorized',
        409: 'User already exists',
        422: 'Cannot create user',
        500: 'Internal Server Error'
    })
    @jwt_required
    def post(self):
        """
        Creates a new user
        """
        return Users.insert_user(api.payload), 201


@api.route('/<string:id>')
class User(Resource):

    @api.marshal_with(user)
    @api.response(404, 'User not found')
    @api.doc(params={'id': 'User ID'})
    @jwt_required
    def get(self, id):
        """
        Get user by ID
        """
        user = Users.get_user(id)
        if not user:
            api.abort(404, 'User not found')
        return user

    @api.doc(responses={
        204: 'No content',
        401: 'Unauthorized',
        404: 'User not found',
        500: 'Internal Server Error'
    }, params={'id': 'User ID'})
    @jwt_required
    def delete(self, id):
        """
        Deletes user by ID
        """
        return Users.delete_user(id)

    @api.expect(user)
    @api.doc(responses={
        204: 'No content',
        400: 'Input payload validation failed',
        401: 'Unauthorized',
        422: 'No user updated',
        500: 'Internal Server Error'
    }, params={'id': 'user ID'})
    @jwt_required
    def put(self, id):
        """
        Updates the user
        """
        return Users.update_user(id, api.payload)
