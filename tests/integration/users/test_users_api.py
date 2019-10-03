import json
from unittest.mock import patch


@patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
def test_get_all_users_endpoint(mock_jwt_required, client):
    response = client.get('/api/v1/users/')
    assert response.status_code == 200


def test_if_get_all_users_without_jwt_fails(client):
    response = client.get('/api/v1/users/')
    assert response.status_code == 401


@patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
def test_get_single_user_endpoint(mock_jwt_required, client):
    response = client.get('/api/v1/users/')
    user_id = response.json[0].get('id')
    response = client.get(f'/api/v1/users/{user_id}')
    assert response.status_code == 200
    response = client.get(f'/api/v1/users/54759eb3c090d83494e2d804')
    assert response.status_code == 404


def test_if_get_single_users_without_jwt_fails(client):
    response = client.get(f'/api/v1/users/54759eb3c090d83494e2d804')
    assert response.status_code == 401


@patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
def test_create_and_delete_user_endpoints(mock_jwt_required, user_list, json_headers, client):

    def create_user(user):
        created = client.post('/api/v1/users/', data=json.dumps(user), headers=json_headers)
        assert created.status_code == 201
        conflict = client.post('/api/v1/users/', data=json.dumps(user), headers=json_headers)
        assert conflict.status_code == 409
        bad = client.post('/api/v1/users/', data=json.dumps({'name': 'bla'}), headers=json_headers)
        assert bad.status_code == 400
        return created.json

    def delete_user(user):
        response = client.delete(f'/api/v1/users/{user.get("id")}', headers=json_headers)
        assert response.status_code == 204
        response = client.delete(f'/api/v1/users/{user.get("id")}', headers=json_headers)
        assert response.status_code == 404

    for user in user_list:
        user.pop('id')
        result = create_user(user)
        user.pop('password')
        assert result == user
        delete_user(result)
