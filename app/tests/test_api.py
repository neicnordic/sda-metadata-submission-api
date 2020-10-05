import os
import io
from pathlib import Path
from flask.wrappers import Response
import json
from werkzeug.exceptions import InternalServerError
import requests
import werkzeug


# from tests.conftest import dummy_column_names
# from app.config_dev import MONGODB_DB, MONGODB_DATAPOINTS_COLLECTION, MONGODB_INDICATORS_COLLECTION


def test_upload_file(app, client):
    root_dir = os.path.dirname(__file__)
    right_file = os.path.join(root_dir, '/app/tests/test_files/test_studyDoc.xml')
    wrong_file = os.path.join(root_dir, '/app/tests/test_files/test_runDoc.xml')

    successful_req = {'file': right_file}
    faulty_req = {'file': wrong_file}

    successful_upload = client.post(f'/upload?&object_type=STUDY&files={file:}', data=successful_req,
                                 headers={'Content-Type': 'text/xml'}
                                 )

    assert successful_upload.get_json()['message'] == 200
    # assert success_upload.get_json() == {'message': 'uploading data..'}
    # assert success_replace.get_json() == {'message': 'replacing data..'}
    # assert failing_response.status_code == 400
    # assert no_file_response.get_json() == {'message': 'No file keyword in POST request.'}
