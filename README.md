# Flask Base
[![Build Status](https://travis-ci.org/alefeans/flask-base.svg?branch=master)](https://travis-ci.org/alefeans/flask-base) [![Python](https://img.shields.io/badge/python-3.7-blue.svg)]() [![Python](https://img.shields.io/badge/python-3.6-blue.svg)]() [![MIT License](https://img.shields.io/badge/license-MIT-007EC7.svg?style=flat)](/LICENSE)

My template base to build Flask RESTful APIs using [Flask RESTPlus](https://flask-restplus.readthedocs.io/en/stable/index.html), [JWT Extended](https://flask-jwt-extended.readthedocs.io/en/latest/) and [PyMongo](https://flask-pymongo.readthedocs.io/en/latest/).

You can just clone this repo and start to create/customize your own RESTful API using this code as your template base :)

## JWT, PyMongo... Do i need all of this ???

__NO !__ You can remove JWT, PyMongo and Bcrypt (used for hashing users password on database), excluding all the references on the [app](app/__init__.py), [config](config.py) and the files that makes use of them.

These _"extensions"_ and the _users_ endpoints are there just to help you, if you need to implement all of the boilerplate required to work with JWT, PyMongo and so on.

Don't forget to remove the dependencies from [requirements.txt](requirements.txt) too.

# Getting Started

## Installing

To install the Flask Base you will need to:

```
git clone https://github.com/alefeans/flask-base.git && cd flask-base
pip install -r requirements.txt
```

## Usage

### Development

```
# if you are not using mongo and jwt, forget these exports
export MONGO_URI="<mongodb://<your_mongo_host>:27017/<your_database>"
export JWT_SECRET_KEY="<randomic_key>"
python main.py
```

## Docker


### Build

```
docker build -t flask-app .
```

### Start a New Container

```
docker run -d \
--name flask-app \
-p 5000:5000 \
# if you are not using mongo and jwt, remove the two lines below keeping the 'flask-app' line
-e MONGO_URI="<mongodb://<your_mongo_host>:27017/<your_database>" \
-e JWT_SECRET_KEY="<randomic_key>" \
flask-app
```

## Swagger

After the application goes up, open your browser on `localhost:5000/api/v1/docs` to see the self-documented interactive API:

![](/imgs/swagger.png)


## Project Structure

The project structure is based on the official [Scaling your project](https://flask-restplus.readthedocs.io/en/stable/scaling.html#multiple-apis-with-reusable-namespaces) doc with some adaptations (e.g `v1` folder to agroup versioned resources).


```
.
├── app
│   ├── helpers
│   │   ├── __init__.py
│   │   ├── parsers.py
│   │   └── password.py
│   ├── __init__.py
│   └── v1
│       ├── __init__.py
│       └── resources
│           ├── auth
│           │   ├── __init__.py
│           │   ├── login.py
│           │   └── serializers.py
│           ├── __init__.py
│           └── users
│               ├── __init__.py
│               ├── models.py
│               ├── serializers.py
│               └── user.py
├── config.py
├── Dockerfile
├── LICENSE
├── README.md
├── requirements.txt
├── run.py
├── tests
│   ├── conftest.py
│   ├── fake_data
│   │   └── users.json
│   ├── __init__.py
│   ├── integration
│   │   ├── __init__.py
│   │   └── users
│   │       ├── __init__.py
│   │       └── test_users_api.py
│   └── unit
│       ├── helpers_test
│       │   ├── __init__.py
│       │   └── test_password.py
│       ├── __init__.py
│       └── users
│           ├── __init__.py
│           └── test_users.py
└── tox.ini

```

### Folders

* `app` - All the RESTful API implementation is here.
* `app/helpers` - Useful function/class helpers for all modules.
* `app/v1` - Resource agroupment for all `v1` [Namespaces](https://flask-restplus.readthedocs.io/en/stable/scaling.html#multiple-namespaces).
* `app/v1/resources` - All `v1` resources are implemented here.
* `tests/unit` - Unit tests modules executed on the CI/CD pipeline.
* `tests/integration` - Integration tests modules executed using a fake database on the CI/CD pipeline.
* `tests/fake_data` - Fake data files ("fixtures").

### Files

* `app/__init__.py` - The Flask Application factory (`create_app()`) and it's configuration are done here. Your [Blueprints](https://flask-restplus.readthedocs.io/en/stable/scaling.html#use-with-blueprints) are registered here.
* `app/v1/__init__.py` - The Flask RESTPlus API is created here with the versioned Blueprint (e.g `v1`). Your [Namespaces](https://flask-restplus.readthedocs.io/en/stable/scaling.html#multiple-namespaces) are registered here.
* `config.py` - Config file for envs, global config vars and so on.
* `Dockerfile` - Dockerfile used to build a Docker image (using [Docker Multistage Build](https://docs.docker.com/develop/develop-images/multistage-build/))
* `LICENSE` - MIT License, i.e. you are free to do whatever is needed with the given code with no limits.
* `tox.ini` - Config file for tests using [Tox](https://tox.readthedocs.io/en/latest/index.html).
* `.dockerignore` - Lists files and directories which should be ignored while Docker build process.
* `.gitignore` - Lists files and directories which should not be added to git repository.
* `requirements.txt` - All project dependencies.
* `run.py` - The Application entrypoint.
* `conftest.py` - Common pytest [fixtures](https://docs.pytest.org/en/latest/fixture.html).


### API Versioning

If you need to create another API version (like `/api/v2`), follow these steps:

First, create your `v2` API structure folder:

```
mkdir app/v2
touch app/v2/__init__.py
```

Inside your `app/v2/__init__.py` create your Blueprint:

```
from flask import Blueprint
from flask_restplus import Api

v2_blueprint = Blueprint('v2', __name__, url_prefix='/api/v2')

api = Api(v2_blueprint,
          doc='/docs',
          title='Flask App',
          version='2.0',
          description='Flask RESTful API V2')
```

Create your resources and namespaces inside `app/v2/resources` (like the `app/v1/resources`) and register them:

```
# app/v2/__init__.py

from flask import Blueprint
from flask_restplus import Api

v2_blueprint = Blueprint('v2', __name__, url_prefix='/api/v2')

api = Api(v2_blueprint,
          doc='/docs',
          title='Flask App',
          version='2.0',
          description='Flask RESTful API V2')


# Fictious resource example
from .resources.auth.login import api as auth_ns
api.add_namespace(auth_ns)

```

And finally, register your Blueprint with the Flask Application:

```
# app/__init__.py

# config code...
from app.v1 import v1_blueprint
    app.register_blueprint(v1_blueprint)

from app.v2 import v2_blueprint
    app.register_blueprint(v2_blueprint)

```

Now you have your new endpoints with the base path `/api/v2` :) !

OBS: Your swagger docs for this new API version will be under this base path too. Ex: `localhost:5000/api/v2/docs`.

## Tests

To run the automated tests:

```
# rull all tests stages (with '-q' for a better output)
tox -q

# run unit tests with lint stage
tox -q -- tests/unit

# run integration tests with lint stage
tox -q -- tests/unit

# run only lint stage
tox -q -e lint

# skip lint stage (if u want integration, just modify the directory after '--')
tox -q -e py37 -- tests/unit
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.