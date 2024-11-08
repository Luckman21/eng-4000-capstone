import unittest
import User_Type

# TODO: Test classes
class test_User_Type(unittest.TestCase):

    def test_id(self):
        p1 = User_Type(self)
        self.assertEquals(p1.id == 1)   # TODO: Fill in type

    def test_typename(self):
        p1 = User_Type(self)
        self.assertEquals(p1.user_type == "")   # TODO: Fill in type