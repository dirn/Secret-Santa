"""Management commands"""

from flask.ext.script import Manager

from xmas.factory import create_app
from xmas.manage import CreateEventCommand, CreateUserCommand

manager = Manager(create_app(__name__, ''))
manager.add_command('create_event', CreateEventCommand())
manager.add_command('create_user', CreateUserCommand())

if __name__ == '__main__':
    manager.run()
