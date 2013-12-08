"""Tests for xmas.users.forms."""

import pytest
from werkzeug.datastructures import MultiDict

from xmas.core import db
from xmas.users import forms, models


@pytest.fixture
def user_dict():
    return {
        'name': 'Name',
        'email': 'name@example.org',
    }


def _test_for_required_field(form_class, form_data, field):
    """Test for a required field."""
    del form_data[field]

    form = form_class(MultiDict(form_data))
    assert not form.validate()
    assert field in form.errors


@pytest.mark.usefixtures('context')
def test_profileform(user_dict):
    """Test `ProfileForm`."""
    form = forms.ProfileForm(MultiDict(user_dict))
    assert form.validate()


@pytest.mark.usefixtures('context')
def test_profileform_invalid_email(user_dict):
    """Test `ProfileForm` with an invalid email."""
    user_dict['email'] = 'email'
    form = forms.ProfileForm(MultiDict(user_dict))
    assert not form.validate()
    assert 'email' in form.errors


@pytest.mark.usefixtures('context')
def test_profileform_no_email(user_dict):
    """Test `ProfileForm` with no `email`."""
    _test_for_required_field(forms.ProfileForm, user_dict, 'email')


@pytest.mark.usefixtures('context')
def test_profileform_repeated_email(user_dict):
    """Test `ProfileForm` with an `email` that already exists."""
    user = models.User()
    db.session.add(user)
    for key, value in user_dict.items():
        setattr(user, key, value)
    db.session.commit()

    form = forms.ProfileForm(MultiDict(user_dict))
    assert not form.validate()
    assert 'email' in form.errors


@pytest.mark.usefixtures('context')
def test_profileform_no_name(user_dict):
    """Test `ProfileForm` with no `name`."""
    _test_for_required_field(forms.ProfileForm, user_dict, 'name')
