import os

DEBUG = bool(os.environ.get('DEBUG', True))

DATABASE_HOST = os.environ.get('DATABASE_HOST', '127.0.0.1')
DATABASE_PORT = int(os.environ.get('DATABASE_PORT', '27017'))
# DATABASE_USER = os.environ.get('DATABASE_USER', None)
# DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD', None)
DATABASE_NAME = os.environ.get('DATABASE_NAME', 'currenciesapidb')