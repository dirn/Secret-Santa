"""A Secret Santa web application."""

# import os

# from flask import Flask
# from flask.ext.bootstrap import Bootstrap
# from flask.ext.simon import Simon


# # Make the app before anything else
# app = Flask(__name__)

# secrets = os.path.abspath(os.path.join(os.path.dirname(__file__),
#                                        os.pardir, 'secrets.cfg'))
# try:
#     app.config.from_pyfile(secrets)
# except IOError:
#     pass

# from .utils import config

# app.secret_key = config('FLASK_SECRET_KEY', 'grOdiymojN7A2G')

# app.config['BOOTSTRAP_GOOGLE_ANALYTICS_ACCOUNT'] = config('GA_PROFILE')
# app.config['BOOTSTRAP_JQUERY_VERSION'] = '1.9.0'
# Bootstrap(app)

# Simon(app)

# from .models import login_manager
# login_manager.setup_app(app)

# from . import views
