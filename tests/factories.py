"""Factory for populating models for tests."""

import factory
from factory.alchemy import SQLAlchemyModelFactory

from xmas import models
from xmas.core import db
from xmas.utils import slugify


class Event(SQLAlchemyModelFactory):

    """Return an instance of :class:`~xmas.models.Event`."""

    FACTORY_FOR = models.Event
    FACTORY_SESSION = db.session

    id = factory.Sequence(lambda x: x)
    name = factory.Sequence(lambda x: 'Event {}'.format(x))
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))


class Item(SQLAlchemyModelFactory):

    """Return an instance of :class:`~xmas.models.Item`."""

    FACTORY_FOR = models.Item
    FACTORY_SESSION = db.session

    id = factory.Sequence(lambda x: x)
    name = factory.Sequence(lambda x: 'Item {}'.format(x))


class User(SQLAlchemyModelFactory):

    """Return an instance of :class:`~xmas.models.User`."""

    FACTORY_FOR = models.User
    FACTORY_SESSION = db.session

    id = factory.Sequence(lambda x: x)
    name = factory.Sequence(lambda x: 'User {}'.format(x))
    email = factory.Sequence(lambda x: 'email-{}@example.org'.format(x))
