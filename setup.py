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
        'Flask-Admin==1.0.7',
        'Flask-Bootstrap==3.0.2.3',
        'Flask-Login==0.2.7',
        'Flask-Mail==0.9.0',
        'Flask-Principal==0.4.0',
        'Flask-SQLAlchemy==1.0',
        'Flask-Script==0.6.6',
        'Flask-Security==1.6.9',
        'Flask-WTF==0.9.3',
        'Jinja2==2.7.1',
        'Mako==0.9.0',
        'MarkupSafe==0.18',
        'SQLAlchemy==0.8.4',
        'WTForms==1.0.5',
        'Werkzeug==0.9.4',
        'alembic==0.6.1',
        'blinker==1.3',
        'gunicorn==18.0',
        'itsdangerous==0.23',
        'newrelic==2.6.0.5',
        'raven==3.6.0',
        'passlib==1.6.1',
        'psycopg2==2.5.1',
        'pytz==2013.8',
    ],
    tests_require=['tox'],
    cmdclass={'test': Tox},
    license=read_file('LICENSE'),
    classifiers=[
    ],
)
