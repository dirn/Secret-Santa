"""Users views."""

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask.ext.login import current_user

from xmas.core import db
from xmas.forms import ProfileForm
from xmas.frontend import route

__all__ = 'blueprint',

blueprint = Blueprint('users', __name__)


@route(blueprint, '/profile', methods=('GET', 'POST'))
def profile():
    """Return the user's profile."""
    form = ProfileForm(request.form, obj=current_user)
    if form.validate_on_submit():
        form.populate_obj(current_user)
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('users.profile'))
    return render_template('users/profile.html', form=form)
