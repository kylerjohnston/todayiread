#!/usr/bin/env python

from kylereads import create_app, db
from kylereads.models import User, ReadingSession, Title
from flask.ext.script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
import os

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app = app,
                db = db,
                User = User,
                ReadingSession = ReadingSession,
                Title = Title)

manager.add_command('shell',
                    Shell(make_context = make_shell_context))

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
