import os

class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost/bookdb')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost/testdb')
    TESTING = True
    DEBUG = False