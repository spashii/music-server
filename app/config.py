import os
base_dir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a very secret key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or \
                              'sqlite:///' + os.path.join(base_dir, 'site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TRACK_CACHE_PATH = os.environ.get('TRACK_CACHE_PATH') or \
                 os.path.join(base_dir, 'track_cache')
