import math
import sys
import unittest

sys.path.insert(0, '../')

from lib import haversine

class Test_Haversine(unittest.TestCase):
    def test_great_circle_distance(self):
        expected = 0.0
        actual = haversine.great_circle_distance(
            math.pi,
            math.pi/2.0, 
            math.pi, 
            math.pi/2.0
        )
        self.assertEquals(expected, actual)

    def test_haversine_function(self):
        expected = 1.0
        actual = haversine.haversine_function(
            math.pi,
            2*math.pi
        )
        self.assertEquals(expected, actual)

    def test_haversine_formula(self):
        expected = 0.0
        actual = haversine.haversine_formula(
            2*math.pi,
            math.pi,
            math.pi,
            2*math.pi
        )
        self.assertEquals(expected, actual)

if __name__ == '__main__':
    unittest.main()
