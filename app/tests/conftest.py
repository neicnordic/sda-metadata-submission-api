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

test_indicators_base = OrderedDict({
    'display': [True, True],
    'source': ['AMR', 'FAO', 'ES'],
    'category': ['Health', 'Economics'],
    'subcategory': ['Antibiotics', 'Trade'],
    'name': ['name', 'type'],
    'type': ['amino', 'gemino', 'income', 'outcome']
})

country_codes = {'Denmark': 'DEN',
                 'Iceland': 'ISL',
                 'Japan': 'JAP'
                 }

subcategories = {'Health': 'Antibiotics',
                 'Economics': 'Trade',
                 }

regions = {'Denmark': 'Europe',
           'Iceland': 'Northern Europe',
           'Japan': 'Asia'}

income_groups = {'Denmark': 'High',
                 'Iceland': 'Higher',
                 'Japan': 'Intermediate'}

dummy_column_names = ['subcategory', 'category', 'year', 'source', 'country code',
                      'country']


@pytest.fixture(scope='session')
def mongodb_connection():
    yield pymongo.MongoClient(
        DB_URI,
        username=MONGODB_USER,
        password=MONGODB_PASS,
    )


@pytest.fixture()
def mongodb_session(mongodb_connection, request):
    """
    Creates a fake MongoDB to use for testing. Populates the DB with data base on `test_records_base`, in two databases
    called "Test_DB1" and "Test_DB2". Both test databases have one collection, called "TestCollection".

    NOTE: This will cleanup all non-default data in the database before and after the actual test runs.

    TODO:
        Remove redundancy in tests.DB_URI and having DB_URI in `app`, so can just grab DB_URI from `app` here directly.
        Means splitting this fixture into `db_connection` and `db_session`, where `db_connection` is session scopedþ
        And in `db_session`, having a finalizer that cleans up data.
    """

    def cleanup_db():
        for db_name in mongodb_connection.list_database_names():
            if db_name not in ('admin', 'config', 'local'):
                mongodb_connection.drop_database(db_name)

    column_names = list(test_datapoints_records_base.keys()) + ["country code"] + ["region"] + ["income group"]

    test_db = mongodb_connection[MONGODB_DB]

    test_datapoints_collection = test_db[MONGODB_DATAPOINTS_COLLECTION]
    test_indicators_collection = test_db[MONGODB_INDICATORS_COLLECTION]

    records_datapoints_gen_obj = product(*test_datapoints_records_base.values())
    records__indicators_gen_obj = product(*test_indicators_base.values())

    for obj in records_datapoints_gen_obj:
        obj = list(obj) + [country_codes.get(obj[0])] + \
              [regions.get(obj[0])] + [income_groups.get(obj[0])]

        dict_obj = dict(zip(column_names, obj))
        test_datapoints_collection.insert_one(dict_obj)

    for obj in records__indicators_gen_obj:
        dict_obj = dict(zip(test_indicators_base.keys(), obj))
        test_indicators_collection.insert_one(dict_obj)

    test_indicators_collection.create_index([("$**", "text")])
    request.addfinalizer(cleanup_db)

    return mongodb_connection


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
def collection_state():
    """
    Gives back a mock object that can be queried like an actual pymongo mongodb client.

    For example:

        ```
        mock_collection = collection_state()
        query_iterator = collection.find({'country': 'Iceland'})
        for document in query_iterator:
            print(document)

        {'country': 'Iceland', 'year': 1999, ...}
        ```
    """
    collection_mock = mongomock.MongoClient().db.collection
    records_gen_obj = product(*test_datapoints_records_base.values())
    column_names = list(test_datapoints_records_base.keys()) + ['country code']
    for obj in records_gen_obj:
        obj = list(obj) + [country_codes.get(obj[0])]
        dict_obj = dict(zip(column_names, obj))
        collection_mock.insert_one(dict_obj)
    return collection_mock


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
