import unittest
import Material

# TODO: Test classes
class test_Material(unittest.TestCase):

    def test_id(self):
        p1 = Material(self)
        self.assertEquals(p1.id == 1)   # TODO: Fill in type

    def test_colour(self):
        p1 = Material(self)
        self.assertEquals(p1.colour == "")   # TODO: Fill in type

    def test_name(self):
        p1 = Material(self)
        self.assertEquals(p1.name == "")    # TODO: Fill in type

    def test_mass(self):
        p1 = Material(self)
        self.assertEquals(p1.mass == 1)   # TODO: Fill in type