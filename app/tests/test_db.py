from pymongo import MongoClient


def test_get_db(app):
    with app.app_context():
        from app.db import mongo
        client = mongo.cx
        assert isinstance(client, MongoClient)
        assert client.address[1] == 27017
        assert 'admin' in client.list_database_names()

    return None
