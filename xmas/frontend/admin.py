"""The admin."""

from flask import redirect, request, url_for
from flask.ext.admin import Admin
from flask.ext.admin.base import MenuLink, expose
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.login import current_user

from xmas.core import db
from xmas.models import Event, Role, User

__all__ = 'init_app',


def date_formatter(view, context, model, name):
    return getattr(model, name).strftime('%b %d, %Y')


class AuthenticatedMenuLink(MenuLink):

    """Only show a link to authenticated users."""

    def is_accessible(self):
        return current_user.is_authenticated()


class NotAuthenticatedMenuLink(MenuLink):

    """Only show a link to unauthenticated users."""

    def is_accessible(self):
        return not current_user.is_authenticated()


class EventModelView(ModelView):

    """Admin for :class:`~xmas.models.Event`."""

    column_formatters = {
        'begins': date_formatter,
        'ends': date_formatter,
    }
    column_list = ('name', 'slug', 'begins', 'ends', 'active', 'locked')
    column_searchable_list = ('name',)

    form_excluded_columns = ('event',)

    list_template = 'admin/events/event/list.html'

    @expose('/assign/', methods=('GET', 'POST'))
    def assign_recipients(self):
        return_url = request.args.get('url') or url_for('.index_view')

        if not self.can_edit:
            return redirect(return_url)

        id = request.args.get('id')
        if id is None:
            return redirect(return_url)

        model = self.get_one(id)

        if model is None:
            return redirect(return_url)

        model.assign_recipients()

        return redirect(return_url)

    @expose('/lock/', methods=('GET', 'POST'))
    def lock(self):
        return_url = request.args.get('url') or url_for('.index_view')

        if not self.can_edit:
            return redirect(return_url)

        id = request.args.get('id')
        if id is None:
            return redirect(return_url)

        model = self.get_one(id)

        if model is None:
            return redirect(return_url)

        model.lock()

        return redirect(return_url)


class UserModelView(ModelView):

    """Admin for :class:`~xmas.models.User`."""

    # can_create = False

    column_list = ('name', 'email', 'active')
    column_searchable_list = ('name', 'email')

    form_columns = ('name', 'email', 'active', 'roles')


def init_app(app):
    """Initialize the admin app."""
    admin = Admin(app)

    admin.add_view(EventModelView(Event, db.session, 'Events'))
    admin.add_view(UserModelView(User, db.session, 'Users'))
    admin.add_view(ModelView(Role, db.session, 'Roles'))

    admin.add_link(
        NotAuthenticatedMenuLink(name='Login', endpoint='security.login')
    )
    admin.add_link(
        AuthenticatedMenuLink(name='Logout', endpoint='security.logout')
    )
