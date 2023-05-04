import unittest
import unittest.mock

from flask import Flask

import main


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)

    def test_random_commander(self):
        with self.app.app_context():
            request = unittest.mock.Mock(args={})
            response = main.random_commander(request)
            assert response.status_code == 200
            assert response.get_json()

    def test_random_commander_Pauper(self):
        with self.app.app_context():
            request = unittest.mock.Mock(args={'format': 'pauperbrawl'})
            response = main.random_commander(request)
            assert response.status_code == 200

            json = response.get_json()
            assert json
            assert json['rarity'] == 'uncommon'


if __name__ == '__main__':
    unittest.main()
