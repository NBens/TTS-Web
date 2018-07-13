class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'DEVELOPMENT KEY'
    DATABASE_HOST = 'localhost'
    DATABASE_USER = 'postgres'
    DATABASE_PASSWORD = 'postgres'
    DATABASE_NAME = 'netbsd'

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

