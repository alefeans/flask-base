import json
import pytest
from app import create_app
from flask_restplus import marshal
from app.v1.resources.users.serializers import create_user


@pytest.fixture(scope='session')
def client():
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()
    yield client


@pytest.fixture(scope='module')
def user_list():
    """
    Reads the data from 'users.json' file,
    marshalling with the 'create_user' serializer.
    In this way, we can assert that our fake test
    will produce the same fields of our serializer.

    Yields:
        list: List of parsed users objects (dict).
    """
    with open('tests/fake_data/users.json', 'r') as fp:
        data = json.loads(fp.read())
        yield marshal(data, create_user)
