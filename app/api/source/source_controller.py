import csv
from flask import request, jsonify
from app.config_dev import MONGODB_DB, MONGODB_METADATA_COLLECTION
from app import db
from app import utils
from app.constants import INVALID_XML, MISSING_FILE_KEY, MISSING_FILE_NAME
from app.exceptions import CustomError
from io import TextIOWrapper


def upload_file():
    """
    Check if the post request has a file part (which should include filename as well). If either is not supplised, then
    redirect to the base URL.

    If the payload has both parts, check if the file has the correct extension. Secure the filename (i.e. avoiding
    '../..' in it) and save it to the upload folder.

    :return: Redirect the user to base url OR return successful status code.
    """

    db_client = db.mongo.cx
    args = request.args.to_dict()
    object_type = args['object_type']
    object_type.lower()
    metadata_collection = db_client[MONGODB_DB][MONGODB_METADATA_COLLECTION]

    if 'file' not in request.form:
        raise CustomError(MISSING_FILE_KEY)
    file = request.form['file']

    if request.form['filename'] == '':
        raise CustomError(MISSING_FILE_NAME)
    file_extension_ok = utils.is_file_extension_allowed(request.form['filename'])
    if not file_extension_ok:
        raise CustomeError(INCORRECT_FILE_TYPE)

    fstring = file
    xml_valid = utils.is_valid_xml(fstring.encode(), object_type)
    # TODO: turn the file to XML format, check validity and split to xml nodes, instead of each line being one record

    if xml_valid:
        utils.collection_writer(fstring, object_type, 'metadatadb', metadata_collection)
        return jsonify({"message": "uploading data.."}), 200
    else:
        raise CustomError(INVALID_XML)
