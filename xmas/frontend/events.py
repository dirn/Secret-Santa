"""Events views."""

from flask import (
    abort, Blueprint, redirect, render_template, request, url_for
)
from flask.ext.login import current_user

from xmas.core import db
from xmas.forms import ItemForm
from xmas.frontend import route
from xmas.models import Event, EventRecipient, Item, ItemClaim

__all__ = 'blueprint',

blueprint = Blueprint('events', __name__)


@route(blueprint, '/claim', methods=('POST',))
def claim():
    """Mark an item as claimed."""
    item = Item.query.get(request.form.get('id'))
    if item.user_id == current_user.id:
        abort(403)
    event = Event.query.get(item.event_id)
    if not event.active:
        abort(404)

    quantity = max(int(request.form.get('quantity', 0)), 1)

    item.claim(current_user, quantity)
    return render_template('events/item.html', item=item)


@route(blueprint, '/<string:slug>/shopping-list')
def claims(slug):
    """Return a user's shopping list for the event."""
    event = Event.query.filter(Event.slug == slug).first_or_404()
    claims = ItemClaim.query.filter(
        Item.event_id == event.id,
        ItemClaim.user_id == current_user.id,
    )
    return render_template(
        'events/claims.html', event=event, claims=claims,
    )


@route(
    blueprint,
    '/<string:slug>/wishlist/<int:id_>',
    methods=('DELETE', 'GET', 'POST', 'PUT'),
)
def edit_wishlist(slug, id_):
    """Return an editable item."""
    event = Event.query.filter(Event.slug == slug).first_or_404()
    item = Item.query.filter(Item.id == id_).first_or_404()

    if item.user_id != current_user.id:
        abort(403)

    if request.method == 'DELETE':
        db.session.delete(item)
        db.session.commit()
        return 'OK'

    form = ItemForm(request.form, item)
    if form.validate_on_submit():
        form.populate_obj(item)
        db.session.commit()
        if request.method == 'PUT':
            return 'OK'
        return redirect(url_for('events.wishlist', slug=slug))

    return render_template('events/edit_item.html', event=event, form=form)


@route(blueprint, '/purchase', methods=('PUT',))
def purchase():
    """Make an item as purchased."""
    item = Item.query.get(request.form.get('id'))
    if item.user_id == current_user.id:
        abort(404)
    event = Event.query.get(item.event_id)
    if not event.active:
        abort(404)

    item.mark_purchased(current_user)
    return render_template('events/item.html', item=item)


@route(blueprint, '/return', methods=('PUT',))
def unpurchase():
    """Make an item as not purchased."""
    item = Item.query.get(request.form.get('id'))
    if item.user_id == current_user.id:
        abort(404)
    event = Event.query.get(item.event_id)
    if not event.active:
        abort(404)

    item.mark_unpurchased(current_user)
    return render_template('events/item.html', item=item)


# TODO: Change the method to DELETE
@route(blueprint, '/unclaim', methods=('POST',))
def unclaim():
    """Remove the claim on an item."""
    item = Item.query.get(request.form.get('id'))
    if item.user_id == current_user.id:
        abort(403)
    event = Event.query.get(item.event_id)
    if not event.active:
        abort(404)

    item.unclaim(current_user)
    return render_template('events/item.html', item=item)


@route(blueprint, '/<string:slug>')
def view(slug, show_all=False):
    """Return the detailed view of the event."""
    event = Event.query.filter_by(slug=slug).first_or_404()

    # Load all of the event's recipients.
    recipients = EventRecipient.query.filter_by(event=event)
    if show_all:
        # If showing all recipients, filter out the current user and get
        # a unique list.
        recipients = recipients.filter(
            EventRecipient.recipient != current_user
        ).distinct(
            EventRecipient.event_id, EventRecipient.recipient_id
        )
    else:
        # Otherwise get only the recipients assigned to the current
        # user.
        recipients = recipients.filter_by(user=current_user)

    # Sort the recipients by name
    recipients = sorted(recipients, key=lambda r: r.recipient.name)

    return render_template(
        'events/view.html', event=event, recipients=recipients
    )


@route(blueprint, '/<string:slug>/stocking-stuffers')
def view_all_users(slug):
    """Return the detailed view of the event with all other users."""
    return view(slug, show_all=True)


@route(blueprint, '/<string:slug>/wishlist', methods=('GET', 'POST'))
def wishlist(slug):
    """Return the current user's wishlist."""
    event = Event.query.filter(Event.slug == slug).first_or_404()

    form = ItemForm(request.form)
    if form.validate_on_submit():
        if form.id.data:
            item = Item.query.get(form.id.data)
        else:
            item = Item()
        form.populate_obj(item)
        if not form.id.data:
            item.id = None
            item.event_id = event.id
            item.user_id = current_user.id
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('events.wishlist', slug=slug))

    wishlist = Item.query.filter(
        Item.event_id == event.id, Item.user_id == current_user.id,
    ).all()
    return render_template(
        'events/wishlist.html', event=event, form=form, items=wishlist,
    )
