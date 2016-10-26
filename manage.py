#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Management script."""
import datetime
import os
from glob import glob
from subprocess import call

from flask import url_for
from flask_migrate import Migrate, MigrateCommand
from flask_script import Command, Manager, Option, Server, Shell
from flask_script.commands import Clean, ShowUrls

from packr.app import create_app
from packr.extensions import db
from packr.models import Role
from packr.models import User
from packr.settings import DevConfig, ProdConfig, TestConfig

CONFIG = ProdConfig if os.environ.get('PACKR_ENV') == 'prod' else DevConfig
HERE = os.path.abspath(os.path.dirname(__file__))
TEST_PATH = os.path.join(HERE, 'tests')

app = create_app(CONFIG)
manager = Manager(app)
migrate = Migrate(app, db)


@manager.command
def list_routes():
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        url = url_for(rule.endpoint, **options)
        output.append(url)

    for line in sorted(output):
        print(line)


def _make_context():
    """Return context dict for a shell session with app, db, and the User."""
    return {'app': app, 'db': db}


@manager.command
def test():
    """Run the tests."""
    import pytest
    CONFIG = TestConfig  # noqa
    exit_code = pytest.main([TEST_PATH, '--verbose'])
    return exit_code


@manager.command
def reset():
    """Reset the stuff."""
    import shutil
    from packr.settings import TestConfig
    try:
        if os.path.exists('migrations'):
            shutil.rmtree('migrations')
        if os.path.isfile(TestConfig.DB_PATH):
            os.remove(TestConfig.DB_PATH)
        if os.path.isfile(DevConfig.DB_PATH):
            os.remove(DevConfig.DB_PATH)
    except Exception as e:
        print(e.with_traceback())
        return 1
    return 0


@manager.command
def setup_db():
    """Setup the database with initial values"""

    for line in open('setup.sql'):
        db.session.execute(line)
        db.session.commit()


@manager.command
def make_admin_account(email, password, firstname, lastname):
    """Created an admin account"""

    admin_role = Role.query.filter_by(role_name='admin').first()

    user = User(email=email,
                password=password,
                firstname=firstname,
                lastname=lastname,
                role=admin_role,
                created_at=datetime.datetime.utcnow())

    user.save()


class Lint(Command):
    """Lint and check code style with flake8 and isort."""

    def get_options(self):
        """Command line options."""
        return (
            Option('-f', '--fix-imports', action='store_true',
                   dest='fix_imports',
                   default=False,
                   help='Fix imports using isort, before linting'),
        )

    def run(self, fix_imports):
        """Run command."""
        skip = ['requirements']
        root_files = glob('*.py')
        root_directories = [name for name in next(os.walk('.'))[1]
                            if not name.startswith('.')]
        files_and_directories = [arg for arg in root_files + root_directories
                                 if arg not in skip]

        def execute_tool(description, *args):
            """Execute a checking tool with its arguments."""
            command_line = list(args) + files_and_directories
            print('{}: {}'.format(description, ' '.join(command_line)))
            rv = call(command_line)
            if rv is not 0:
                exit(rv)

        if fix_imports:
            execute_tool('Fixing import order', 'isort',
                         '-sg', 'migrations',
                         '-sg', 'node_modules',
                         '-rc')
            execute_tool('Checking code style', 'flake8',
                         '--exclude', 'node_modules,migrations')


manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)
manager.add_command('urls', ShowUrls())
manager.add_command('clean', Clean())
manager.add_command('lint', Lint())

if __name__ == '__main__':
    manager.run()
