"""Factory for populating models for tests."""

from xmas import models as _models
from xmas.core import db as _db


def _factory(cls, kwargs):
    """Return an instance of ``cls``."""
    obj = cls()
    for key, value in kwargs.items():
        setattr(obj, key, value)
    _db.session.add(obj)
    return obj


def event(**kwargs):
    """Return an instance of :class:`~xmas.models.Event`."""
    return _factory(_models.Event, kwargs)


def user(**kwargs):
    """Return an instance of :class:`~xmas.models.User`."""
    return _factory(_models.User, kwargs)
