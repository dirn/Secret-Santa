"""Tests for xmas.events.models."""

from datetime import datetime, timedelta

import pytest
from sqlalchemy import distinct, func

from tests import factories
from xmas.core import db
from xmas.events import models


@pytest.fixture(scope='module')
def today():
    # Dates throughout are handled in UTC.
    return datetime.utcnow().date()


@pytest.mark.usefixtures('context')
def test_event_assign_recipients():
    """Test `Event.assign_recipients()`."""
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


@pytest.mark.usefixtures('context')
def test_event_assign_recipients_locked():
    """Test `Event.assign_recipients()` with a locked event."""
    user1 = factories.user()
    user2 = factories.user()

    event = factories.event(locked=True, number_of_recipients=1)

    event.users.extend((user1, user2))

    event.assign_recipients()

    assert not models.EventRecipient.query.all()


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


@pytest.mark.usefixtures('context')
def test_item_claim():
    """Test `Item.claim()`."""
    user = factories.user()
    item = factories.item(quantity=1)

    db.session.commit()

    claim = item.claim(user, quantity=1)

    assert item.quantity_claimed == 1

    assert claim.quantity == 1
    assert claim.item_id == item.id
    assert claim.user_id == user.id


@pytest.mark.usefixtures('context')
def test_item_claim_none_available():
    """Test `Item.claim()` with no quantity_remaining."""
    user = factories.user()
    item = factories.item(quantity=1, quantity_claimed=1)

    db.session.commit()

    claim = item.claim(user, quantity=1)

    assert claim is None


@pytest.mark.usefixtures('context')
def test_item_claim_too_many():
    """Test `Item.claim()` with a quantity that's too large."""
    user = factories.user()
    item = factories.item(quantity=1)

    db.session.commit()

    claim = item.claim(user, quantity=10)

    assert item.quantity_claimed == 1

    assert claim.quantity == 1


@pytest.mark.usefixtures('context')
def test_item_claim_unlimited():
    """Test `Item.claim()` with an item with unlimited quantity."""
    user = factories.user()
    item = factories.item(quantity=0)

    db.session.commit()

    claim = item.claim(user, quantity=1)

    assert item.quantity_claimed == 1

    assert claim.quantity == 1


@pytest.mark.usefixtures('context')
def test_item_is_claimed():
    """Test `Item.is_claimed()`."""
    user = factories.user()
    item = factories.item()
    db.session.commit()

    item.claim(user, quantity=1)

    assert item.is_claimed(user.id)


@pytest.mark.usefixtures('context')
def test_item_is_claimed_unclaimed():
    """Test `Item.is_claimed()` with an unclaimed user."""
    user1 = factories.user()
    user2 = factories.user()
    item = factories.item()
    db.session.commit()

    item.claim(user1, quantity=1)

    assert not item.is_claimed(user2.id)


@pytest.mark.usefixtures('context')
def test_item_is_purchased():
    """Test `Item.is_purchased()`."""
    user = factories.user()
    item = factories.item()
    db.session.commit()

    item.claim(user, quantity=1)
    item.mark_purchased(user)

    assert item.is_purchased(user.id)


@pytest.mark.usefixtures('context')
def test_item_is_purchased_unclaimed():
    """Test `Item.is_purchased()` with an unclaimed item."""
    user = factories.user()
    item = factories.item()
    db.session.commit()

    item.mark_purchased(user)

    assert not item.is_purchased(user.id)


@pytest.mark.usefixtures('context')
def test_item_mark_purchased():
    """Test `Item.mark_purchased()`."""
    user = factories.user()
    item = factories.item()
    db.session.commit()

    claim = item.claim(user, quantity=1)
    item.mark_purchased(user)

    assert claim.purchased


@pytest.mark.usefixtures('context')
def test_item_mark_unpurchased():
    """Test `Item.mark_unpurchased()`."""
    user = factories.user()
    item = factories.item()
    db.session.commit()

    claim = item.claim(user, quantity=1)
    claim.purchased = True
    item.mark_unpurchased(user)

    assert not claim.purchased


@pytest.mark.usefixtures('context')
def test_item_quantity_claimed_by_user():
    """Test `Item.quantity_claimed_by_user()`."""
    user = factories.user()
    item = factories.item()
    db.session.commit()

    item.claim(user, quantity=1)

    assert item.quantity_claimed_by_user(user.id) == 1


@pytest.mark.usefixtures('context')
def test_item_quantity_claimed_by_user_unclaimed():
    """Test `Item.quantity_claimed_by_user()` by an unclaimed user."""
    user1 = factories.user()
    user2 = factories.user()
    item = factories.item()
    db.session.commit()

    item.claim(user1, quantity=1)

    assert item.quantity_claimed_by_user(user2.id) == 0


@pytest.mark.usefixtures('context')
def test_item_unclaim():
    """Test `Item.unclaim()`."""
    user = factories.user()
    item = factories.item(quantity=10)
    db.session.commit()

    item.claim(user, quantity=5)
    item.unclaim(user)

    assert item.quantity_claimed == 0


@pytest.mark.usefixtures('context')
def test_item__user_claim():
    """Test `Item._user_claim()`."""
    user = factories.user()
    item = factories.item()
    db.session.commit()

    expected = item.claim(user, quantity=1)
    actual = item._user_claim(user.id)

    assert actual == expected
