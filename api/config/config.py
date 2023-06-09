import os
import re
from decouple import config
from datetime import timedelta
# import psycopg2
# from distutils.debug import DEBUG



# BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# db_name = 'student_db'


# default_uri = "postgres://{}:{}@{}/{}".format('postgres', 'piperlead', 'localhost:5432', db_name)

# uri = os.getenv('DATABASE_URL', default_uri) # or other relevant config var
# uri = config('DATABASE_URL')  # or other relevant config var
# if uri.startswith('postgres://'):
#     uri = uri.replace('postgres://', 'postgresql://', 1)

# class Config:
#     SECRET_KEY = config('SECRET_KEY', 'secret')
#     JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
#     JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=30)
#     JWT_SECRET_KEY = config('JWT_SECRET_KEY')

# class DevConfig(Config):
#     DEBUG = True
#     SQLALCHEMY_TRACK_MODIFICATION = False
#     SQLALCHEMY_ECHO =True
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(BASE_DIR, 'db.sqlite3')


# class TestConfig(Config):
#     TESTING = True
#     SQLALCHEMY_TRACK_MODIFICATION = False
#     SQLALCHEMY_ECHO =True
#     SQLALCHEMY_DATABASE_URI = 'postgres://postgres:piperlead@127.0.0.1:5432/student_db'



# class ProdConfig(Config):
#     SQLALCHEMY_DATABASE_URI = uri
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     DEBUG = config('DEBUG', False, cast=bool)


# config_dict ={
#     'dev': DevConfig,
#     'prod': ProdConfig,
#     'test': TestConfig
# }




import os
from decouple import config
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

uri = os.environ.get('DATABASE_URL') # or other relevant config var
if uri and uri.startswith('postgres://'):
    uri = uri.replace('postgres://', 'postgresql://', 1)

class Config:
    SECRET_KEY = config('SECRET_KEY', 'secret')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=14)
    JWT_SECRET_KEY = config('JWT_SECRET_KEY')

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(BASE_DIR, 'db.sqlite3')

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = config('DEBUG', False, cast=bool)
    
config_dict = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig
}