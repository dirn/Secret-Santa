"""Events models."""

import datetime
import random

from xmas.core import db
from xmas.users.models import User

__all__ = 'Event', 'EventRecipient', 'Item'

events_users = db.Table(
    'events_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('event_id', db.Integer(), db.ForeignKey('events.id')),
)


class Event(db.Model):

    """Events."""

    __tablename__ = 'events'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    slug = db.Column(db.String(50), unique=True)
    begins = db.Column(db.Date())
    ends = db.Column(db.Date())
    number_of_recipients = db.Column(db.SmallInteger())
    suggested_limit = db.Column(db.Float())
    active = db.Column(db.Boolean())
    locked = db.Column(db.Boolean())

    users = db.relationship(
        'User',
        secondary=events_users,
        backref=db.backref('events', lazy='dynamic'),
    )

    def __str__(self):
        """Return the friendly representation."""
        return self.name

    def assign_recipients(self):
        """Assign recipients to all users for the event."""
        if self.locked:
            return

        total = len(self.users)
        maximum = min(self.number_of_recipients, total - 1)

        # Generate a copy of all the users.
        users = self.users[:]
        # Randomize it.
        random.shuffle(users)
        # And extend it.
        users *= 2

        recipients = {
            users[x]: users[x + 1:x + maximum + 1] for x in range(total)
        }
        # givers = {
        #     k2: [k for k, v in recipients.items() if k2 in v] for k2 in {
        #         a for b in recipients.values() for a in b
        #     }
        # }

        for k, v in recipients.items():
            k.event_recipients = [EventRecipient(self, k, u) for u in v]

        self.lock(commit=False)

        db.session.commit()

    @property
    def is_still_active(self):
        """Returns whether the event is still editable by users."""
        now = datetime.datetime.utcnow().date()
        if self.active and self.begins <= now < self.ends:
            return True
        return False

    def lock(self, commit=True):
        """Mark the event as locked."""
        if self.locked:
            return

        self.locked = True

        if commit:
            db.session.commit()


class EventRecipient(db.Model):

    """Event recipients."""

    __tablename__ = 'event_recipients'

    event_id = db.Column(
        db.Integer(), db.ForeignKey('events.id'), primary_key=True,
    )
    user_id = db.Column(
        db.Integer(), db.ForeignKey('users.id'), primary_key=True,
    )
    recipient_id = db.Column(
        db.Integer(), db.ForeignKey('users.id'), primary_key=True,
    )

    event = db.relationship(
        'Event',
        primaryjoin=event_id == Event.id,
        backref=db.backref('event', lazy='dynamic'),
    )
    user = db.relationship(
        'User',
        primaryjoin=user_id == User.id,
        backref=db.backref('user', lazy='dynamic'),
    )
    recipient = db.relationship(
        'User',
        primaryjoin=recipient_id == User.id,
        backref=db.backref('recipient', lazy='dynamic'),
    )
    wishlist = db.relationship(
        'Item',
        primaryjoin='and_(EventRecipient.event_id == Item.event_id, '
                    '     EventRecipient.recipient_id == Item.user_id)',
        backref=db.backref('wishlist', lazy='dynamic', uselist=True),
    )

    __table_args__ = (
        db.UniqueConstraint('event_id', 'user_id', 'recipient_id'),
    )

    def __init__(self, event, user, recipient):
        self.event = event
        self.user = user
        self.recipient = recipient

    def __str__(self):
        """Return the friendly representation."""
        return '{} is giving to {}'.format(self.user.name, self.recipient.name)


class Item(db.Model):

    """Wishlist items."""

    __tablename__ = 'event_items'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.Text())
    cost = db.Column(db.Float())
    quantity = db.Column(db.Integer())
    quantity_claimed = db.Column(db.Integer(), default=0)
    active = db.Column(db.Boolean(), default=True)
    url = db.Column(db.String(255))
    event_id = db.Column(db.Integer())
    user_id = db.Column(db.Integer())

    claims = db.relationship(
        'ItemClaim',
        backref=db.backref('claims', lazy='dynamic', uselist=True),
    )
    recipient = db.relationship(
        'EventRecipient',
        primaryjoin='and_(Item.event_id == EventRecipient.event_id,'
                    '     Item.user_id == EventRecipient.recipient_id)',
    )

    __table_args__ = (
        db.ForeignKeyConstraint(
            (event_id, user_id),
            (EventRecipient.event_id, EventRecipient.recipient_id),
            name='fk_wishlist',
            use_alter=True,
        ),
    )

    def __str__(self):
        """Return the friendly representation."""
        return self.name

    def claim(self, user, quantity=1):
        """Claim an item."""
        if self.is_claimed(user.id):
            # Change the claim.
            return

        if self.quantity and self.quantity_claimed + quantity > self.quantity:
            # Raise an exception.
            return

        db.session.query(Item).filter(Item.id == self.id).update({
            Item.quantity_claimed: Item.quantity_claimed + quantity,
        })

        self.claims.append(ItemClaim(self, user, quantity))
        db.session.commit()

    def is_claimed(self, user_id):
        return any(c.user_id == user_id for c in self.claims)

    def is_purchased(self, user_id):
        return any(c.user_id == user_id for c in self.claims if c.purchased)

    def mark_purchased(self, user):
        if not self.is_claimed(user.id):
            # Raise an exception.
            pass
        elif self.is_purchased(user.id):
            # Raise an exception.
            pass
        else:
            claim = ItemClaim.query.filter(
                ItemClaim.item_id == self.id,
                ItemClaim.user_id == user.id,
            ).one()
            claim.purchased = True
            db.session.commit()

    def mark_unpurchased(self, user):
        if not self.is_claimed(user.id):
            # Raise an exception.
            pass
        elif not self.is_purchased(user.id):
            # Raise an exception.
            pass
        else:
            claim = ItemClaim.query.filter(
                ItemClaim.item_id == self.id,
                ItemClaim.user_id == user.id,
            ).one()
            claim.purchased = False
            db.session.commit()

    def unclaim(self, user):
        """Remove a claim from an item."""
        if not self.is_claimed(user.id):
            # Raise an exception.
            return

        claim = ItemClaim.query.filter(
            ItemClaim.item_id == self.id,
            ItemClaim.user_id == user.id,
        ).one()

        db.session.query(Item).filter(Item.id == self.id).update({
            Item.quantity_claimed: Item.quantity_claimed - claim.quantity,
        })

        db.session.delete(claim)
        db.session.commit()


class ItemClaim(db.Model):

    """Claimed wishlist items."""

    __tablename__ = 'event_item_claims'

    item_id = db.Column(
        db.Integer(), db.ForeignKey('event_items.id'), primary_key=True,
    )
    user_id = db.Column(
        db.Integer(), db.ForeignKey('users.id'), primary_key=True,
    )
    quantity = db.Column(db.Integer())
    purchased = db.Column(db.Boolean())

    item = db.relationship('Item', primaryjoin=item_id == Item.id)
    user = db.relationship('User')

    __table_args__ = (
        db.UniqueConstraint('item_id', 'user_id'),
    )

    def __init__(self, item, user, quantity):
        self.item = item
        self.user = user
        self.quantity = quantity

    def __str__(self):
        """Return the friendly representation."""
        print(dir(self.item))
        return '{} has claimed {} for {}.'.format(
            self.user,
            self.item,
            self.item.recipient.recipient.name,
        )
