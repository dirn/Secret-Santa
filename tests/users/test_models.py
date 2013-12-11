"""Tests for xmas.users.models."""

import pytest

from tests import factories
from xmas.core import db
from xmas.users import models


@pytest.mark.usefixtures('context')
def test_user___eq__():
    """Test `User.__eq__()`."""
    user1 = factories.User()
    db.session.commit()
    user2 = models.User.query.get(user1.id)
    assert user1 == user2


@pytest.mark.usefixtures('context')
def test_user___eq___no_id():
    """Test `User.__eq__()` with no `id`."""
    user1 = factories.User(id=None)
    user2 = factories.User(id=None)
    assert user1 == user2


@pytest.mark.usefixtures('context')
def test_user___eq___unequal():
    """Test `User.__eq__()` with different users."""
    user1 = factories.User()
    user2 = factories.User()
    db.session.commit()
    # == needs to be used.
    assert not (user1 == user2)


@pytest.mark.usefixtures('context')
def test_user___hash__():
    """Test `User.__hash__()`."""
    user1 = factories.User()
    user2 = factories.User()
    db.session.commit()
    # The implementation shouldn't matter.
    assert hash(user1) == hash(user1)  # Should be repeatable
    assert hash(user1) != hash(user2)


@pytest.mark.usefixtures('context')
def test_user___ne__():
    """Test `User.__ne__()`."""
    user1 = factories.User()
    user2 = factories.User()
    db.session.commit()
    assert user1 != user2


@pytest.mark.usefixtures('context')
def test_user___ne___equal():
    """Test `User.__ne__()` with the same user."""
    user1 = factories.User()
    db.session.commit()
    user2 = models.User.query.get(user1.id)
    # != needs to be used.
    assert not (user1 != user2)


@pytest.mark.usefixtures('context')
def test_user___ne___no_id():
    """Test `User.__ne__()` with no `id`."""
    user1 = factories.User(id=None)
    user2 = factories.User(id=None)
    # != needs to be used
    assert not (user1 != user2)
