import os
import sys
import logging
from logging.config import dictConfig

logger = logging.getLogger(__name__)


dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "[%(levelname)s] - [%(asctime)s] - %(name)s - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
        }
    },
    "loggers": {
        "werkzeug": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["console"]
    }
})


class BaseConfig:

    DEBUG = True
    RESTPLUS_VALIDATE = True
    JWT_CLAIMS_IN_REFRESH_TOKEN = True
    ERROR_INCLUDE_MESSAGE = False
    RESTPLUS_MASK_SWAGGER = False
    PROPAGATE_EXCEPTIONS = True

    try:
        MONGO_URI = os.environ['MONGO_URI']
        JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
    except KeyError as key:
        logger.critical(f'{key} env var is missing !')
        sys.exit()


class ProdConfig(BaseConfig):

    DEBUG = False


class DevConfig(BaseConfig):
    pass
