import os
import sys
import unittest

sys.path.insert(0, '../')

import main

db_fd = None

def setUpModule():
    main.app.config['DATABASE'] = 'test'
    main.init_db()

def tearDownModule():
    if db_fd:
        os.close(db_fd)
        os.unlink(main.app.config['DATABASE'])

class Test_Main(unittest.TestCase):
    def setUp(self):
        main.app.config['TESTING'] = True
        self.app = main.app.test_client()

    def test_foodtrucks(self):
        expected = 'Cupkates'
        actual = self.app.get('/api/foodtrucks?latitude=37.7901490737255&longitude=-122.398658184604&distance=0.0').data
        self.assertIn(expected, actual)

    def test_foodtrucks_no_data(self):
        expected = 'Bad Request'
        actual = self.app.get('/api/foodtrucks').data
        self.assertIn(expected, actual)

    def test_foodtrucks_empty_data(self):
        expected = 'Bad Request'
        actual = self.app.get('/api/foodtrucks?latitude=&longitude=&distance=').data
        self.assertIn(expected, actual)

    def test_foodtrucks_bad_data(self):
        expected = 'Bad Request'
        actual = self.app.get('/api/foodtrucks?latitude=test&longitude=0.0&=distance=not_a_float').data
        self.assertIn(expected, actual)
