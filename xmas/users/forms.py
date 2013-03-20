"""User forms."""

from flask.ext.wtf import Form
from wtforms.fields import HiddenField, TextField
from wtforms.validators import Email, Required

from xmas.models import User
from xmas.validators import Unique

__all__ = 'ProfileForm',


class ProfileForm(Form):

    """Form for editing :class:`~xmas.models.User` instances."""

    id = HiddenField()
    name = TextField('Name', validators=(Required(),))
    email = TextField('Email', validators=(
        Required(),
        Email(),
        Unique(User, 'email'),
    ))
