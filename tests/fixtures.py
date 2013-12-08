"""Test fixtures."""

import pytest

from tests import settings
from xmas.core import db
from xmas.factory import create_app


@pytest.fixture
def context(request):
    """Return an application context."""
    app = create_app(__name__, '', settings)
    context = app.app_context()
    context.push()

    # Build all database tables.
    db.create_all()

    def tear_down():
        # Drop all database tables.
        db.drop_all()
        context.pop()
    request.addfinalizer(tear_down)

    return context
