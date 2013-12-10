"""Application helper utilities."""

import importlib
from operator import truth
import pkgutil
import re

from flask import Blueprint

__all__ = 'register_blueprints', 'slugify'

slug_pattern = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


def register_blueprints(app, package_name, package_path):
    """Register all :class:`Flask.Blueprint` instances on the app."""
    for _, name, _ in pkgutil.iter_modules(package_path):
        m = importlib.import_module('{}.{}'.format(package_name, name))
        for x in dir(m):
            item = getattr(m, x)
            if isinstance(item, Blueprint):
                app.register_blueprint(item)


def slugify(value, delimiter='-'):
    """Return a slugified version of the specified string."""
    words = slug_pattern.split(value)
    return delimiter.join(filter(truth, words)).lower()
