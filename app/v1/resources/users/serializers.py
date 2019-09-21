from app.v1 import api
from flask_restplus import fields


user = api.model('User', {
    'id': fields.String(readonly=True, description='User ID', attribute='_id.$oid'),
    'username': fields.String(description='User Name'),
    'email': fields.String(description='User Email')
})
