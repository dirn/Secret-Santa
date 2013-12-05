"""Frontend application."""

from functools import wraps

from flask import render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.security import login_required
from raven.contrib.flask import Sentry

from xmas import factory
from xmas.frontend import admin, filters

__all__ = 'create_app', 'route'


def create_app(settings_override=None):
    """Return the Secret Santa frontend application.

    :param settings_override: a ``dict`` of settings to override.

    """
    app = factory.create_app(__name__, __path__, settings_override)

    Bootstrap(app)
    admin.init_app(app)
    filters.init_app(app)
    Sentry(app)

    if not app.debug:
        for e in (404, 500):
            app.errorhandler(e)(handle_error)

    return app


def handle_error(error):
    """Return the render error template."""
    return render_template('errors/{}.html'.format(error.code)), error.code


def route(blueprint, *args, **kwargs):
    """Return a route."""
    def decorator(f):
        @blueprint.route(*args, **kwargs)
        @login_required
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        return f
    return decorator
