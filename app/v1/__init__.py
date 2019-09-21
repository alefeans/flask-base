from flask import Blueprint
from flask_restplus import Api

v1_blueprint = Blueprint('v1', __name__, url_prefix='/api/v1')

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
}

api = Api(v1_blueprint,
          doc='/docs',
          title='Flask App',
          version='1.0',
          description='Flask RESTful API',
          security='Bearer Auth',
          authorizations=authorizations)

from .resources.auth.login import api as auth_ns
from .resources.users.user import api as user_ns

api.add_namespace(auth_ns)
api.add_namespace(user_ns)
