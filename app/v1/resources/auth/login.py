from flask_restplus import Resource, Namespace
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, get_jwt_claims
from app import mongo, jwt
from app.helpers import refresh_parser, check_password
from .serializers import login, full_token, acc_token

api = Namespace('auth', 'Authentication')


@api.route('/login')
class Login(Resource):

    @api.marshal_with(full_token)
    @api.expect(login)
    @api.doc(responses={
        200: 'Success',
        400: 'Username or password is a required property',
        404: 'User not found',
        401: 'Unauthorized'
    }, security=None)
    def post(self):
        """
        Authentication endpoint
        """
        username = api.payload.get('username')
        password = api.payload.get('password')

        user = mongo.db.users.find_one({'username': username}, {'_id': 0})

        if not user:
            api.abort(404, 'User not found')

        if not check_password(password, user.get('password')):
            api.abort(401, 'Unauthorized')

        access_token = create_access_token(identity=user)
        refresh_token = create_refresh_token(identity=user)
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'name': user.get('name'),
        }


@api.route('/refresh')
class TokenRefresh(Resource):
    @jwt_refresh_token_required
    @api.expect(refresh_parser)
    @api.doc(responses={
        424: 'Invalid refresh token'
    }, security=None)
    @api.response(200, 'Success', acc_token)
    def post(self):
        """
        Retrieve Access Token using Refresh Token
        """
        claims = get_jwt_claims()
        claims['username'] = get_jwt_identity()
        access_token = create_access_token(identity=claims)
        return {'access_token': access_token}


@jwt.user_claims_loader
def add_claims_to_access_token(user):
    return {'privilege': user.get('privilege')}


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user['username']
