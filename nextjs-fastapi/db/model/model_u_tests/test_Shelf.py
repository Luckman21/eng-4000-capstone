import unittest
import Shelf

# TODO: Test classes
class test_Shelf(unittest.TestCase):

    def test_id(self):
        p1 = Shelf(self)
        self.assertEquals(p1.id == 1)   # TODO: Fill in type

    def test_humid(self):
        p1 = Shelf(self)
        self.assertEquals(p1.humidity_pct == 1.0)   # TODO: Fill in type

    def test_temp(self):
        p1 = Shelf(self)
        self.assertEquals(p1.temperature_cel == 1.0)    # TODO: Fill in type