"""Tests for xmas.users.forms."""

import pytest
from werkzeug.datastructures import MultiDict

from tests.fixtures import context  # Needed for Unique check.
from xmas.core import db
from xmas.users import forms, models


@pytest.fixture
def user_dict():
    return {
        'name': 'Name',
        'email': 'name@example.org',
    }


def _test_for_required_field(context, form_class, form_data, field):
    """Test for a required field."""
    del form_data[field]

    form = form_class(MultiDict(form_data))
    assert not form.validate()
    assert field in form.errors


def test_profileform(context, user_dict):
    """Test `ProfileForm`."""
    form = forms.ProfileForm(MultiDict(user_dict))
    assert form.validate()


def test_profileform_invalid_email(context, user_dict):
    """Test `ProfileForm` with an invalid email."""
    user_dict['email'] = 'email'
    form = forms.ProfileForm(MultiDict(user_dict))
    assert not form.validate()
    assert 'email' in form.errors


def test_profileform_no_email(context, user_dict):
    """Test `ProfileForm` with no `email`."""
    _test_for_required_field(context, forms.ProfileForm, user_dict, 'email')


def test_profileform_repeated_email(context, user_dict):
    """Test `ProfileForm` with an `email` that already exists."""
    user = models.User()
    db.session.add(user)
    for key, value in user_dict.items():
        setattr(user, key, value)
    db.session.commit()

    form = forms.ProfileForm(MultiDict(user_dict))
    assert not form.validate()
    assert 'email' in form.errors


def test_profileform_no_name(context, user_dict):
    """Test `ProfileForm` with no `name`."""
    _test_for_required_field(context, forms.ProfileForm, user_dict, 'name')
