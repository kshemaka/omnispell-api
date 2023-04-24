import unittest
import unittest.mock

from flask import Flask

import main


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)

    def test_random_commander(self):
        with self.app.app_context():
            request = unittest.mock.Mock()
            response = main.random_commander(request)
            assert response.status_code == 200
            assert response.get_json()


if __name__ == '__main__':
    unittest.main()
