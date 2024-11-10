import unittest
import Material_Type

# TODO: Test classes
class test_Material_Type(unittest.TestCase):

    def test_id(self):
        p1 = Material_Type(self)
        self.assertEquals(p1.id == 1)   # TODO: Fill in type

    def test_name(self):
        p1 = Material_Type(self)
        self.assertEquals(p1.name == "")    # TODO: Fill in type