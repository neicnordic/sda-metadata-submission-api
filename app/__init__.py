from app.api.source.source_router import source_blueprint
import logging
import os

from flask import Flask, Response
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from app.exceptions import make_json_error

from app.api.source.source_router import source_blueprint

__all__ = ["create_app"]


class ReverseProxied(object):

    """Middleware for handling reverse proxied setups."""

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = environ.get("HTTP_X_SCRIPT_NAME", "")
        forwarded_proto = environ.get("HTTP_X_FORWARDED_PROTO", "")
        forwarded_for = environ.get("HTTP_X_FORWARDED_FOR", "").split(",")[0]
        forwarded_host = environ.get("HTTP_X_FORWARDED_HOST", "")

        if script_name:
            environ["SCRIPT_NAME"] = script_name
        if forwarded_for is not None:
            environ["REMOTE_ADDR"] = forwarded_for
        if forwarded_host:
            environ["HTTP_HOST"] = forwarded_host
        if forwarded_proto:
            environ["wsgi.url_scheme"] = forwarded_proto
        return self.app(environ, start_response)


def create_app(test_config=None):
    app = Flask(__name__)
    app.wsgi_app = ReverseProxied(app.wsgi_app)
    app.config.from_object('app.config_dev')

    if test_config:
        app.config.from_mapping(test_config)
    from .db import mongo
    mongo.init_app(
        app,
        uri=app.config["DB_URI"],
    )

    @app.errorhandler(HTTPException)
    def handle_http_exceptions(ex) -> Response:
        """Handler for :py:class:`werkzeug.exceptions.HTTPException`.

        This function ensures we always respond with a JSON payload when any
        :py:class:`werkzeug.exceptions.HTTPException is thrown.

        """
        # Only create new error response if the exception does not already have
        # its own response defined.
        if ex.response is not None:
            return ex

        if ex.code == 500:
            app.logger.exception(ex)

        return make_json_error(ex)

    app.register_error_handler(400, lambda e: 'bad request!')

    app.register_blueprint(source_blueprint)

    cors = CORS()
    cors.init_app(app)

    # if in production
    if not app.debug:
        from logging.handlers import TimedRotatingFileHandler

        file_handler = TimedRotatingFileHandler(os.path.join(app.config['LOG_DIR'], 'app.log'), 'midnight')
        file_handler.setLevel(logging.WARNING)
        file_handler.setFormatter(logging.Formatter('<%(asctime)s> <%(levelname)s> %(message)s'))
        app.logger.addHandler(file_handler)

    return app
