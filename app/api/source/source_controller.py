import csv
import re
from io import StringIO
from lxml import etree
from flask import request, jsonify
from app.config_dev import MONGODB_DB, MONGODB_METADATA_COLLECTION
from app import db
from app import utils
from app.constants import INVALID_XML, MISSING_FILE_KEY, MISSING_FILE_NAME
from app.exceptions import CustomError
from io import TextIOWrapper
from werkzeug.datastructures import FileStorage


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

    if 'file' not in request.files:
        raise CustomError(MISSING_FILE_KEY)
    file = request.files['file']

    if request.form['filename'] == '':
        raise CustomError(MISSING_FILE_NAME)
    file_extension_ok = utils.is_file_extension_allowed(request.form['filename'])
    if not file_extension_ok:
        raise CustomeError(INCORRECT_FILE_TYPE)

    fstring = file.read().decode('utf-8')
    print(fstring)
    is_referenced = utils.is_referenced_object_registered(fstring, object_type, metadata_collection)
    accession_id = re.search('accession_id=(.+?)filename', fstring).group(1)
    file_type = re.search('accession_id=(.+?)checksum', fstring).group(1)

    if not is_referenced:
        return jsonify({"message": "this document can not be uploaded since it's not being referenced anywhere"}), 400
    xml_valid = utils.is_valid_xml(fstring, object_type)
    # TODO: turn the file to XML format, check validity and split to xml nodes, instead of each line being one record

    if xml_valid:
        utils.collection_writer(fstring, object_type, metadata_collection)
        return jsonify(
            {"message": f"The file {accession_id} of type {file_type} was successfully uploaded", "data": [accession_id,
             file_type]}), 200
    else:
        return jsonify({"Something went wrong with your submission, please check each field's requirements"}), 400
