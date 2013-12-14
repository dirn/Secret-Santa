"""Custom validators."""

import re

from sqlalchemy.orm.exc import NoResultFound
from wtforms.validators import ValidationError

__all__ = 'DefaultValue', 'Slugify', 'Unique'


class DefaultValue:

    """Sets a default value for a field."""

    def __init__(self, default):
        self.default = default

    def __call__(self, form, field):
        if field.data is None:
            field.data = self.default


class Slugify:

    """Makes a slug from another field."""

    # From http://flask.pocoo.org/snippets/5/
    _punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')

    def __init__(self, field, delimiter='-', message=None):
        self.field = field

        self.delimiter = delimiter

        if message is None:
            message = 'A slug cannot be created from {}.'.format(self.field)
        self.message = message

    def __call__(self, form, field):
        if field.data:
            return

        value = getattr(form, self.field, None)

        if value is None or not value.data:
            raise ValidationError(self.message)

        words = self._punct_re.split(value.data)
        field.data = self.delimiter.join(words).lower()


class Unique:

    """Checks that a value is unique for a model."""

    def __init__(self, model, field, message=None):
        self.model = model
        self.field = field

        if message is None:
            message = '{} must be unique.'.format(self.field.title())
        self.message = message

    def __call__(self, form, field):
        try:
            query = (getattr(self.model, self.field) == field.data,)
            if form.id.data:
                query += (self.model.id != form.id.data,)
            self.model.query.filter(*query).one()
        except NoResultFound:
            pass
        else:
            raise ValidationError(self.message)


defaultvalue = DefaultValue
slugify = Slugify
unique = Unique
