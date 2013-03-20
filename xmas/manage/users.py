"""User-related management commands."""

import sys

from flask.ext.script import Command, prompt, prompt_pass
from flask.ext.security.forms import RegisterForm
from flask.ext.security.registerable import register_user
from werkzeug.datastructures import MultiDict


class CreateUserCommand(Command):

    """Create a user."""

    def run(self):
        email = prompt('Email')
        name = prompt('Name')
        password = prompt_pass('Password')
        password_confirm = prompt_pass('Confirm Password')
        data = MultiDict({
            'email': email,
            'password': password,
            'password_confirm': password_confirm,
        })
        form = RegisterForm(data, csrf_enabled=False)
        if form.validate():
            user = register_user(name=name, email=email, password=password)
            print('\nUser created successfully.')
            print('User(id={} email={})'.format(user.id, user.email))
            return
        print('\nError creating user:')
        for errors in form.errors.values():
            print('\n'.join(errors))
        sys.exit(1)
