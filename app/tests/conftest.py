from collections import OrderedDict
from itertools import product

import mongomock
import pymongo
import pytest

from app import create_app
from app.tests import DB_URI, MONGODB_USER, MONGODB_PASS
from app.config_dev import MONGODB_METADATA_COLLECTION, MONGODB_DB

test_datapoints_records_base = OrderedDict({
    'country': ['Denmark', 'Iceland', 'Japan'],
    'year': [1999, 2010, 2018],
    'someColumn': ['column_value_1', 'column_value_2'],
    'value': [10, 5, 7],
    'display': [True],
    'value unit': ['kg', 'liters'],
    'source': ['AMR', 'FAO', 'ES'],
    'category': ['Health', 'Economics'],
    'subcategory': ['Antibiotics', 'Trade'],
    'indicator': [{'name': 'amino'}, {'name': 'gemino'},
                  {'type': 'income'}, {'type': 'outcome'}]
})


@pytest.fixture(scope='session')
def mongodb_connection():
    yield pymongo.MongoClient(
        DB_URI,
        username=MONGODB_USER,
        password=MONGODB_PASS,
    )


@pytest.fixture()
def make_temp_file(tmp_path):
    """
    Creates an empty test directory to write files to an a test directory with a stub file for testing.

    :return: A tuple of (empty_test_dir_path, testfile_path).
    """

    test_dir = tmp_path / 'tmp_file_folder'
    test_dir.mkdir()

    testfile_path = test_dir / 'testfile.csv'
    testfile_path.write_text('Raiden\n' * 50)

    return testfile_path


@pytest.fixture()
def make_empty_folder(tmp_path):
    empty_test_dir = tmp_path / 'tmp_empty_folder'
    empty_test_dir.mkdir()

    return empty_test_dir


@pytest.fixture()
def app(make_empty_folder):
    app = create_app({'TESTING': True,
                      'UPLOAD_FOLDER': make_empty_folder,
                      'MONGODB_USER': MONGODB_USER,
                      'MONGODB_PASS': MONGODB_PASS,
                      })

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
