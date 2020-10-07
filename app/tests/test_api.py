import os
import io
from pathlib import Path
from werkzeug.exceptions import InternalServerError
import werkzeug
import requests
from lxml import etree
from io import StringIO


def test_upload_file(client):
    root_dir = os.path.dirname(__file__)
    right_file = os.path.join(root_dir, 'test_files/test_studyDoc.xml')
    wrong_file = os.path.join(root_dir, 'test_files/test_runDoc.xml')

    successful_doc = {'file': (io.StringIO(str(Path(__file__).parent /
                                               right_file)).read(),
                               'test_studyDoc.xml'), }

    faulty_doc = {'file': (io.StringIO(str(Path(__file__).parent /
                                           wrong_file)).read(),
                           'test_runDoc.xml'), }

    successful_upload = client.post('/upload?&object_type=STUDY', data=successful_doc,
                                    content_type='multipart/form-data'
                                    )

    faulty_upload = client.post('/upload?&object_type=STUDY', data=faulty_doc,
                                content_type='multipart/form-data'
                                )

    assert successful_upload.get_json()['message'] == 'The file  of type  was successfully uploaded'
    assert faulty_upload.get_json()['message'] == 'The submitted form is not valid'
