"""Application settings."""

from os import environ as _env

DEBUG = _env.get('DEBUG', '').lower() == 'true'
SECRET_KEY = _env.get('SECRET_KEY', 'You need to define a secret key')

# Miscellaneous
GOOGLE_ANALYTICS_ACCOUNT = _env.get('GOOGLE_ANALYTICS_ACCOUNT')
GOOGLE_ANALYTICS_DOMAIN = _env.get('GOOGLE_ANALYTICS_DOMAIN')

# Flask-Mail
MAIL_SERVER = _env.get('MAIL_SERVER', 'localhost')
MAIL_PORT = int(_env.get('MAIL_PORT', 25))
MAIL_USERNAME = _env.get('MAIL_USERNAME')
MAIL_PASSWORD = _env.get('MAIL_PASSWORD')
MAIL_USE_SSL = _env.get('MAIL_USE_SSL', '').lower() != 'false'
MAIL_USE_TLS = _env.get('MAIL_USE_TLS', '').lower() != 'false'
MAIL_DEBUG = _env.get('MAIL_DEBUG', '').lower() == 'true'
DEFAULT_MAIL_SENDER = _env.get('DEFAULT_MAIL_SENDER')

# Flask-Security
SECURITY_DEFAULT_REMEMBER_ME = True
SECURITY_EMAIL_SENDER = DEFAULT_MAIL_SENDER
SECURITY_EMAIL_SUBJECT_REGISTER = 'Welcome to Secret Santa'
SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
SECURITY_PASSWORD_SALT = _env.get('SECURITY_PASSWORD_SALT', 'Salt goes here')
SECURITY_REGISTERABLE = False
SECURITY_TRACKABLE = True

# Flask-SQLAlchemy
SQLALCHEMY_DATABASE_URI = _env.get('DATABASE_URL')
