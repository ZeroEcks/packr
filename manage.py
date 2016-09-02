import os
from glob import glob
from subprocess import call

from flask_migrate import Migrate, MigrateCommand
from flask_script import Command, Manager, Option

from app import create_app
from app.extensions import db

HERE = os.path.abspath(os.path.dirname(__file__))
TEST_PATH = os.path.join(HERE, 'tests')

app = create_app()

migrate = Migrate(app, db)
manager = Manager(app)


@manager.command
def test():
    """Run the tests."""
    import pytest
    exit_code = pytest.main([TEST_PATH, '--verbose'])
    return exit_code


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
                         '-sg', 'node_modules', '-rc')
            execute_tool('Checking code style', 'flake8',
                         '--exclude', 'node_modules')


manager.add_command('db', MigrateCommand)
manager.add_command('lint', Lint)

if __name__ == '__main__':
    manager.run()
