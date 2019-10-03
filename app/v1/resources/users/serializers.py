from app.v1 import api
from flask_restplus import fields


user = api.model('User', {
    'id': fields.String(readonly=True, description='User ID', attribute='_id.$oid'),
    'username': fields.String(required=True, description='The Username'),
    'email': fields.String(required=True, description='User Email')
})


create_user = api.inherit('User Creation', user, {
    'password': fields.String(required=True, description='User Password'),
})
