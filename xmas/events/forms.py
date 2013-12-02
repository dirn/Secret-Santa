"""Event forms."""

from flask.ext.wtf import Form
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from wtforms.fields import (
    BooleanField, DateField, FloatField, HiddenField, IntegerField,
    SelectMultipleField, TextAreaField, TextField,
)
from wtforms.validators import Optional, Required

from xmas.models import Event, User
from xmas.validators import Slugify, Unique

__all__ = 'EventForm', 'ItemForm'


def default_value(default):
    """Return a validator that sets a default value."""
    def _default(form, field):
        """Set the default value."""
        if field.data is None:
            field.data = default
    return _default


def select_users():
    """Return a :class:`~sqlalchemy.orm.query.Query` of all users."""
    return User.query.order_by(User.email)


class EventForm(Form):

    """Form for editing :class:`~xmas.models.Event` instances."""

    id = HiddenField()
    name = TextField('Name', validators=(Required(),))
    slug = TextField('Slug', validators=(
        Slugify('name'),
        Unique(Event, 'slug'),
        Required(),
    ))
    begins = DateField('Begins on', validators=(Required(),))
    ends = DateField('Ends on', validators=(Required(),))
    number_of_recipients = IntegerField(
        'Number of Recipients', validators=(Required(),),
    )
    suggested_limit = FloatField('Suggested Limit', validators=(Required(),))
    active = BooleanField('Active?')
    users = QuerySelectMultipleField('Users', query_factory=select_users)


class ItemForm(Form):

    """Form for editing :class:`~xmas.models.Item` instances."""

    id = HiddenField()
    name = TextField('Name', validators=(Required(),))
    description = TextAreaField('Description', validators=(Optional(),))
    cost = FloatField('Cost', validators=(Optional(),))
    quantity = IntegerField('Quantity', validators=(
        default_value(1), Optional()
    ))
    url = TextField('URL', validators=(Optional(),))
