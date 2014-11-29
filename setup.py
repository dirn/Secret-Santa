from setuptools import setup
from setuptools.command.test import test as TestCommand


def read_file(filename):
    try:
        with open(filename) as f:
            return f.read()
    except IOError:
        return ''


class Tox(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # Do this import here because tests_require isn't processed
        # early enough to do a module-level import.
        from tox._cmdline import main
        main(self.test_args)


setup(
    name='xmas',
    version='1.0.0',
    description='A Secret Santa web application',
    long_description=read_file('README.rst'),
    author='Andy Dirnberger',
    author_email='dirn@dirnonline.com',
    url='https://github.com/dirn/Secret-Santa',
    packages=['xmas'],
    install_requires=[
        'Flask==0.10.1',
        'Flask-Admin==1.0.8',
        'Flask-Bootstrap==3.0.2.3',
        'Flask-Login==0.2.11',
        'Flask-Mail==0.9.1',
        'Flask-Principal==0.4.0',
        'Flask-SQLAlchemy==2.0',
        'Flask-Script==2.0.5',
        'Flask-Security==1.7.4',
        'Flask-WTF==0.10.3',
        'Jinja2==2.7.3',
        'Mako==1.0.0',
        'MarkupSafe==0.23',
        'SQLAlchemy==0.9.8',
        'WTForms==2.0.1',
        'Werkzeug==0.9.6',
        'alembic==0.7.0',
        'blinker==1.3',
        'itsdangerous==0.24',
        'passlib==1.6.2',
        'psycopg2==2.5.4',
        'pytz==2014.10',
    ],
    tests_require=['tox'],
    cmdclass={'test': Tox},
    license=read_file('LICENSE'),
    classifiers=[
    ],
)
