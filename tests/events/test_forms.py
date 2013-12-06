"""Tests for xmas.events.forms."""

from datetime import date

import pytest
from werkzeug.datastructures import MultiDict

from tests import settings
from xmas.core import db
from xmas.events import forms, models
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


@pytest.fixture
def item_dict():
    return {
        'name': 'Name',
        'description': 'Description',
        'cost': 1.,
        'quantity': 2,  # The default is 1 so use something else.
        'url': 'http://www.example.org',
    }


def _test_for_required_field(app, form_class, form_data, field):
    """Test for a required field."""
    del form_data[field]

    with app.test_request_context():
        db.create_all()
        form = form_class(MultiDict(form_data))
        assert not form.validate()
        assert field in form.errors
        db.drop_all()


def test_eventform(app, event_dict):
    """Test `EventForm`."""
    with app.test_request_context():
        db.create_all()
        form = forms.EventForm(MultiDict(event_dict))
        assert form.validate()
        db.drop_all()


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
        db.create_all()
        form = forms.EventForm(MultiDict(event_dict))
        assert form.validate()
        assert form.slug.data == 'name'
        db.drop_all()


def test_eventform_repeated_slug(app, event_dict):
    """Test `EventForm` with a `slug` that already exists."""
    with app.test_request_context():
        db.create_all()
        event = models.Event()
        db.session.add(event)
        for key, value in event_dict.items():
            if key in ('begins', 'ends'):
                value = date(*map(int, value.split('-')))
            setattr(event, key, value)
        db.session.commit()
        form = forms.EventForm(MultiDict(event_dict))
        assert not form.validate()
        assert 'slug' in form.errors
        db.drop_all()


def test_eventform_no_suggested_limit(app, event_dict):
    """Test `EventForm` with no `suggested_limit`."""
    _test_for_required_field(
        app, forms.EventForm, event_dict, 'suggested_limit'
    )


def test_itemform(app, item_dict):
    """Test `ItemForm`."""
    with app.test_request_context():
        db.create_all()
        form = forms.ItemForm(MultiDict(item_dict))
        assert form.validate()
        db.drop_all()


def test_itemform_no_cost(app, item_dict):
    """Test `ItemForm` with no `cost`."""
    del item_dict['cost']

    with app.test_request_context():
        db.create_all()
        form = forms.ItemForm(MultiDict(item_dict))
        assert form.validate()
        db.drop_all()


def test_itemform_no_description(app, item_dict):
    """Test `ItemForm` with no `description`."""
    del item_dict['description']

    with app.test_request_context():
        db.create_all()
        form = forms.ItemForm(MultiDict(item_dict))
        assert form.validate()
        db.drop_all()


def test_itemform_no_name(app, item_dict):
    """Test `ItemForm` with no `name`."""
    _test_for_required_field(app, forms.ItemForm, item_dict, 'name')


def test_itemform_no_quantity(app, item_dict):
    """Test `ItemForm` with no `quantity`."""
    del item_dict['quantity']

    with app.test_request_context():
        db.create_all()
        form = forms.ItemForm(MultiDict(item_dict))
        assert form.validate()
        assert form.quantity.data == 1
        db.drop_all()


def test_itemform_no_url(app, item_dict):
    """Test `ItemForm` with no `url`."""
    del item_dict['url']

    with app.test_request_context():
        db.create_all()
        form = forms.ItemForm(MultiDict(item_dict))
        assert form.validate()
        db.drop_all()
