"""Application settings."""

from os import environ as _env

DEBUG = _env.get('DEBUG', '').lower() == 'true'
SECRET_KEY = _env.get('SECRET_KEY', 'You need to define a secret key')

# Miscellaneous
GOOGLE_ANALYTICS_ACCOUNT = _env.get('GOOGLE_ANALYTICS_ACCOUNT')
GOOGLE_ANALYTICS_DOMAIN = _env.get('GOOGLE_ANALYTICS_DOMAIN')

# Flask-Security
SECURITY_DEFAULT_REMEMBER_ME = True
SECURITY_EMAIL_SENDER = _env.get('SECURITY_EMAIL_SENDER', 'Email goes here')
SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
SECURITY_PASSWORD_SALT = _env.get('SECURITY_PASSWORD_SALT', 'Salt goes here')
SECURITY_REGISTERABLE = True
SECURITY_TRACKABLE = True

# Flask-SQLAlchemy
SQLALCHEMY_DATABASE_URI = _env.get('DATABASE_URL')
