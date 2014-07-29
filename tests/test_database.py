import sys
import unittest

sys.path.insert(0, '../')

from lib.database import DataBase

ROWS = [
    [
        'test_name_{0}'.format(i), 
        'test_address_{0}'.format(i), 
        'test_fooditems_{0}'.format(i), 
        float(i),
        0.0
    ] for i in range(0, 10)
]

class Test_DataBase(unittest.TestCase):
    def setUp(self):
        self.database = DataBase(':memory:')
        self.database.init_database()
        for row in ROWS:
            self.database.add_row(*row)

    def tearDown(self):
        del self.database

    def test_gen_within_distance(self):
        expected = [
            {
                'name': 'test_name_0',
                'address': 'test_address_0',
                'fooditems': 'test_fooditems_0',
            },
            {
                'name': 'test_name_1',
                'address': 'test_address_1',
                'fooditems': 'test_fooditems_1',
            }
        ]

        actual = [x for x in self.database.gen_within_distance(100.0, 0.0, 0.0)]
        self.assertEquals(expected, actual)

    def test_gen_within_distance_bad_distance(self):
        with self.assertRaises(ValueError):
            [x for x in self.database.gen_within_distance(-1.0, 0.0, 0.0)]

    def test_gen_within_distance_no_results(self):
        expected = []
        actual = [x for x in self.database.gen_within_distance(10.0, 100.0, 100.0)]
        self.assertEquals(expected, actual)

if __name__ == '__main__':
    unittest.main()
