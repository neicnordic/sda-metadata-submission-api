from flask import jsonify
from werkzeug.exceptions import HTTPException


class CustomError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


def make_json_error(ex):
    response = jsonify(message=str(ex))
    response.status_code = (ex.code
                            if isinstance(ex, HTTPException)
                            else 500)
    return response


def handle_exception_type(error):
    """
    Creates an JSON object from the `InvalidUsage` exception object and returns it.

    :param error: The error that was raised, in this case `InvalidUsage.`
    :return A Flask response object with error attributes.
    """
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
