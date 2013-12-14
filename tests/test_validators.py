"""Tests for xmas.validators."""

import pytest
from wtforms.validators import ValidationError

from tests import factories
from xmas import validators
from xmas.core import db
from xmas.models import User


class DummyForm(dict):

    """Based on :class:`~wtforms.tests.validators.DummyForm`."""


class DummyField:

    """Based on :class:`~wtforms.tests.common.DummyField`."""

    def __init__(self, data, errors=(), raw_data=None):
        self.data = data
        self.errors = list(errors)
        self.raw_data = raw_data

    def gettext(self, string):
        return string

    def ngettext(self, singular, plural, n):
        if n == 1:
            return singular
        return plural


@pytest.fixture
def dummy_form():
    return DummyForm()


def test_aliases():
    """Test that validators are aliased properly."""
    assert validators.defaultvalue is validators.DefaultValue
    assert validators.slugify is validators.Slugify
    assert validators.unique is validators.Unique


def test_defaultvalue_none(dummy_form):
    """Test `DefaultValue` with no value."""
    field = DummyField(None)
    assert validators.DefaultValue(1)(dummy_form, field) is None
    assert field.data == 1


def test_defaultvalue_value(dummy_form):
    """Test `DefaultValue` with a value."""
    field = DummyField(20)
    assert validators.DefaultValue(1)(dummy_form, field) is None
    assert field.data == 20


def test_slugify(dummy_form):
    """Test `Slugify`."""
    dummy_form.field = DummyField('This IS A tesT')
    field = DummyField(None)
    assert validators.Slugify('field')(dummy_form, field) is None
    assert field.data == 'this-is-a-test'


def test_slugify_existing_value(dummy_form):
    """Test that `Slugify` doesn't overwrite an existing value."""
    dummy_form.field = DummyField('This IS A tesT')
    field = DummyField('existing-value')
    assert validators.Slugify('field')(dummy_form, field) is None
    assert field.data == 'existing-value'


def test_slugify_validationerror(dummy_form):
    """Test that `Slugify` raises `ValidationError`."""
    dummy_form.field = None
    field = DummyField(None)
    with pytest.raises(ValidationError):
        validators.Slugify('field')(dummy_form, field)


@pytest.mark.usefixtures('context')
def test_unique(dummy_form):
    """Test `Unique`."""
    dummy_form.id = DummyField(None)
    field = DummyField('email@example.org')
    assert validators.Unique(User, 'email')(dummy_form, field) is None


@pytest.mark.usefixtures('context')
def test_unique_existing(dummy_form):
    """Test `Unique` with an existing record."""
    user = factories.User()
    db.session.commit()

    dummy_form.id = DummyField(user.id)
    field = DummyField(user.email)
    assert validators.Unique(User, 'email')(dummy_form, field) is None


@pytest.mark.usefixtures('context')
def test_unique_new(dummy_form):
    """Test `Unique` with a new record."""
    factories.User(email='taken@example.org')
    db.session.commit()

    dummy_form.id = DummyField(None)
    field = DummyField('not-taken@example.org')
    assert validators.Unique(User, 'email')(dummy_form, field) is None


@pytest.mark.usefixtures('context')
def test_unique_validationerror(dummy_form):
    """Test `Unique` raises `ValidationError`."""
    factories.User(email='taken@example.org')
    db.session.commit()

    dummy_form.id = DummyField(None)
    field = DummyField('taken@example.org')
    with pytest.raises(ValidationError):
        validators.Unique(User, 'email')(dummy_form, field)
