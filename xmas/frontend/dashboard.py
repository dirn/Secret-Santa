"""Frontend dashboard."""

from flask import Blueprint, redirect, render_template, url_for
from flask.ext.login import current_user

from xmas.frontend import route
from xmas.models import Event, User

__all__ = 'blueprint',

blueprint = Blueprint(
    'dashboard',
    __name__,
    static_folder='static',
    static_url_path='/frontend/static',
)


@route(blueprint, '/')
def index():
    """Return the dashboard index."""
    events = Event.query.filter(
        Event.active == True,  # NOQA
        Event.users.any(User.id == current_user.id),
    ).order_by(
        Event.begins,
        Event.ends,
    )

    if events.count() == 1:
        # If the user only has one active event, jump straight to it.
        return redirect(url_for('events.view', slug=events[0].slug))

    return render_template('dashboard/index.html', events=events)
