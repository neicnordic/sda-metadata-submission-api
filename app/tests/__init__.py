import os

MONGODB_HOST = os.environ.get('MONGODB_HOST', 'localhost')
MONGODB_PORT = os.environ.get('MONGODB_PORT', '27017')
MONGODB_USER = os.environ.get('MONGODB_USER', 'cge')
MONGODB_PASS = os.environ.get('MONGODB_PASS', 'cge')


DB_URI = f'mongodb://{MONGODB_HOST}:{MONGODB_PORT}/'
