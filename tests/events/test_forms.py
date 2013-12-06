"""Tests for xmas.events.forms."""

import pytest
from werkzeug.datastructures import MultiDict

from tests import settings
from xmas.events import forms
from xmas.factory import create_app


@pytest.fixture
def app():
    return create_app(__name__, '', settings)


@pytest.fixture
def event_dict():
    return {
        'name': 'Name',
        'slug': 'slug',
        'begins': '2013-12-05',
        'ends': '2013-12-05',
        'number_of_recipients': 1,
        'suggested_limit': 1.,
        'active': True,
    }


def _test_for_required_field(app, form_class, form_data, field):
    """Test for a required field."""
    del form_data[field]

    with app.test_request_context():
        form = form_class(MultiDict(form_data))
        assert not form.validate()
        assert field in form.errors


def test_eventform(app, event_dict):
    """Test `EventForm`."""
    with app.test_request_context():
        form = forms.EventForm(MultiDict(event_dict))
        assert form.validate()


def test_eventform_no_begins(app, event_dict):
    """Test `EventForm` with no `begins`."""
    _test_for_required_field(app, forms.EventForm, event_dict, 'begins')


def test_eventform_no_ends(app, event_dict):
    """Test `EventForm` with no `ends`."""
    _test_for_required_field(app, forms.EventForm, event_dict, 'ends')


def test_eventform_no_name(app, event_dict):
    """Test `EventForm` with no `name`."""
    _test_for_required_field(app, forms.EventForm, event_dict, 'name')


def test_eventform_no_number_of_recipients(app, event_dict):
    """Test `EventForm` with no `number_of_recipients`."""
    _test_for_required_field(
        app, forms.EventForm, event_dict, 'number_of_recipients'
    )


def test_eventform_no_slug(app, event_dict):
    """Test `EventForm` with no `slug`."""
    del event_dict['slug']

    with app.test_request_context():
        form = forms.EventForm(MultiDict(event_dict))
        assert form.validate()
        assert form.slug.data == 'name'


def test_eventform_no_suggested_limit(app, event_dict):
    """Test `EventForm` with no `suggested_limit`."""
    _test_for_required_field(
        app, forms.EventForm, event_dict, 'suggested_limit'
    )
