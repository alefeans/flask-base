from app.v1 import api
from flask_restplus import fields


login = api.model('Login', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='User Password')
})

acc_token = api.model('JWT Access Token', {
    'access_token': fields.String(description='Access Token')
})

full_token = api.inherit('JWT Tokens', acc_token, {
    'refresh_token': fields.String(description='Refresh Token'),
})
