"""Test settings."""

DEBUG = False
TESTING = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
SQLALCHEMY_POOL_RECYCLE = None
SQLALCHEMY_POOL_SIZE = None
SQLALCHEMY_POOL_TIMEOUT = None

WTF_CSRF_ENABLED = False
