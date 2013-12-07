"""Tests for xmas.events.models."""

from datetime import datetime, timedelta

import pytest
from sqlalchemy import distinct, func

from tests import factories, settings
from xmas.core import db
from xmas.events import models
from xmas.factory import create_app


@pytest.fixture
def app():
    return create_app(__name__, '', settings)


@pytest.fixture(scope='module')
def today():
    # Dates throughout are handled in UTC.
    return datetime.utcnow().date()


def test_event_assign_recipients(app):
    """Test `Event.assign_recipients()`."""
    with app.test_request_context():
        db.create_all()

        user1 = factories.user()
        user2 = factories.user()
        user3 = factories.user()
        user4 = factories.user()

        event = factories.event(number_of_recipients=2)

        event.users.extend((user1, user2, user3, user4))

        event.assign_recipients()

        # After assigning recipients, the event should be locked.
        assert event.locked

        # Check the number of records.
        expected = len(event.users) * event.number_of_recipients
        actual = models.EventRecipient.query.count()
        assert actual == expected

        # Check the number of users.
        expected = len(event.users)
        actual = db.session.query(
            func.count(distinct(models.EventRecipient.user_id))
        ).first()[0]
        assert actual == expected

        # Check the number of recipients.
        expected = len(event.users)
        actual = db.session.query(
            func.count(distinct(models.EventRecipient.recipient_id))
        ).first()[0]
        assert actual == expected

        # Check that each user has the correct number of recipients.
        expected = event.number_of_recipients
        users = db.session.query(
            func.count(models.EventRecipient.recipient_id)
        ).group_by(models.EventRecipient.user_id).all()
        for actual, *_ in users:
            assert actual == expected

        # Check that each recipient has the correct number of users.
        expected = event.number_of_recipients
        recipients = db.session.query(
            func.count(models.EventRecipient.user_id)
        ).group_by(models.EventRecipient.recipient_id).all()
        for actual, *_ in recipients:
            assert actual == expected

        db.drop_all()


def test_event_assign_recipients_locked(app):
    """Test `Event.assign_recipients()` with a locked event."""
    with app.test_request_context():
        db.create_all()

        user1 = factories.user()
        user2 = factories.user()

        event = factories.event(locked=True, number_of_recipients=1)

        event.users.extend((user1, user2))

        event.assign_recipients()

        assert not models.EventRecipient.query.all()

        db.drop_all()


def test_event_is_still_active(today):
    """Test `Event.is_still_active`."""
    event = models.Event()
    event.active = True
    event.begins = today - timedelta(days=1)
    event.ends = today + timedelta(days=1)
    assert event.is_still_active


def test_event_is_still_active_future(today):
    """Test `Event.is_still_active` with a future date."""
    event = models.Event()
    event.active = True
    event.begins = today + timedelta(days=1)
    event.ends = today + timedelta(days=2)
    assert not event.is_still_active


def test_event_is_still_active_inactive(today):
    """Test `Event.is_still_active` with an inactive event."""
    event = models.Event()
    event.active = False
    event.begins = today - timedelta(days=1)
    event.ends = today + timedelta(days=1)
    assert not event.is_still_active


def test_event_is_still_active_past(today):
    """Test `Event.is_still_active` with a past date."""
    event = models.Event()
    event.active = True
    event.begins = today - timedelta(days=2)
    event.ends = today - timedelta(days=1)
    assert not event.is_still_active


def test_event_lock():
    """Test `Event.lock()`."""
    event = models.Event()
    event.locked = False
    event.lock(commit=False)
    assert event.locked
