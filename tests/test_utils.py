import unittest

import os

import xmas
from xmas.utils import config


class TestConfig(unittest.TestCase):
    """Test the ``config()`` method."""

    def setUp(self):
        xmas.app.config['TESTING'] = True

        xmas.app.config['REAL_KEY_1'] = True
        xmas.app.config['READ_KEY_2'] = '12345'

        os.environ['REAL_ENVIRON_KEY_1'] = 'abcde'

    def test_default(self):
        """Test the ``default`` parameter."""
        with xmas.app.test_request_context():
            # Key found
            self.assertNotEqual(config('REAL_KEY_1', 'value'), 'value')
            self.assertNotEqual(config('REAL_KEY_2', 'value'), '12345')
            # Key not found
            self.assertEqual(config('MADE_UP_KEY_1', 'value'), 'value')

    def test_app_config(self):
        """Test ``app.config``."""
        with xmas.app.test_request_context():
            # Key found
            self.assertEqual(config('REAL_KEY_1', False), True)

    def test_environ(self):
        """Test the fallback to ``os.environ``."""
        with xmas.app.test_request_context():
            # Test that os.environ is used
            self.assertEqual(config('REAL_ENVIRON_KEY_1', 'zyxwv'), 'abcde')

            # Unset the key and make sure it's still in app.config
            os.environ.pop('REAL_ENVIRON_KEY_1')
            self.assertEqual(config('REAL_ENVIRON_KEY_1', 'zyxwv'), 'abcde')

if __name__ == '__main__':
    unittest.main()
