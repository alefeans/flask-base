from functools import wraps
from flask import current_app
from flask_restplus import abort
from flask_jwt_extended import get_jwt_identity, get_jwt_claims


def admin_privilege(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        privilege = get_jwt_claims().get('privilege', '')
        if privilege != 'admin':
            current_app.logger.warning(f'User {get_jwt_identity()} is not a admin')
            abort(401, message='Unauthorized')
        return view(*args, **kwargs)
    return wrapper
