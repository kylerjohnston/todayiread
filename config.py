import os

class Config:
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_SUBJECT_PREFIX = '[Today I Read] '
    MAIL_DEFAULT_SENDER = ('Admin', 'kylerjohnston@gmail.com')

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    SECRET_KEY = 'temporarysecretkey'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////Users/kyle/Code/kylereads/development-data.db'

class TestingConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    TESTING = True
    SQLALCHEMY_DATABASE_URI = ''

class ProductionConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = ''

config = {
    'dev': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
