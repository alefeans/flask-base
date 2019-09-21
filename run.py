import logging
from app import create_app

app = create_app()


if __name__ == "__main__":
    app.run(port=5000)
else:
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
