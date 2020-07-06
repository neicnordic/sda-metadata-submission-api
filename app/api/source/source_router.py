from app.api.source.source_controller import upload_file
from app import exceptions
from flask import Blueprint


source_blueprint = Blueprint('source_blueprint', __name__)

source_blueprint.add_url_rule('/upload', view_func=upload_file, methods=['POST'])
source_blueprint.register_error_handler(exceptions.CustomError, exceptions.handle_exception_type)
