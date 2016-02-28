import os
from env import *

class Config:
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = MAIL_USERNAME
    MAIL_PASSWORD = MAIL_PASSWORD
    DB_USERNAME = DB_USERNAME
    DB_PASSWORD = DB_PASSWORD
    SECRET_KEY = SECRET_KEY
    MAIL_SUBJECT_PREFIX = '[Today I Read] '
    MAIL_DEFAULT_SENDER = ('Admin', MAIL_USERNAME)

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////Users/kyle/Code/kylereads/development-data.db'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = ''

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://' + Config.DB_USERNAME + ':' + Config.DB_PASSWORD + '@localhost/' + Config.DB_USERNAME

config = {
    'dev': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
