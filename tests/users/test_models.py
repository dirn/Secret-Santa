"""Tests for xmas.users.models."""

from tests import factories
from tests.fixtures import context
from xmas.core import db
from xmas.users import models


def test_user___eq__(context):
    """Test `User.__eq__()`."""
    user1 = factories.user()
    db.session.commit()
    user2 = models.User.query.get(user1.id)
    assert user1 == user2


def test_user___eq___no_id(context):
    """Test `User.__eq__()` with no `id`."""
    user1 = factories.user()
    user2 = factories.user()
    assert user1 == user2


def test_user___eq___unequal(context):
    """Test `User.__eq__()` with different users."""
    user1 = factories.user()
    user2 = factories.user()
    db.session.commit()
    # == needs to be used.
    assert not (user1 == user2)


def test_user___hash__(context):
    """Test `User.__hash__()`."""
    user1 = factories.user()
    user2 = factories.user()
    db.session.commit()
    # The implementation shouldn't matter.
    assert hash(user1) == hash(user1)  # Should be repeatable
    assert hash(user1) != hash(user2)


def test_user___ne__(context):
    """Test `User.__ne__()`."""
    user1 = factories.user()
    user2 = factories.user()
    db.session.commit()
    assert user1 != user2


def test_user___ne___equal(context):
    """Test `User.__ne__()` with the same user."""
    user1 = factories.user()
    db.session.commit()
    user2 = models.User.query.get(user1.id)
    # != needs to be used.
    assert not (user1 != user2)


def test_user___ne___no_id(context):
    """Test `User.__ne__()` with no `id`."""
    user1 = factories.user()
    user2 = factories.user()
    # != needs to be used
    assert not (user1 != user2)
