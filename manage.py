"""Management commands"""

from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager

from xmas.core import db
from xmas.factory import create_app
from xmas.manage import CreateEventCommand, CreateUserCommand

app = create_app(__name__, '')
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('create_event', CreateEventCommand())
manager.add_command('create_user', CreateUserCommand())
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
