# config.py
class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///jokes.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
