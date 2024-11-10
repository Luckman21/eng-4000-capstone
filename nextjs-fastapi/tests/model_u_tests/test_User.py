import unittest
import User

# TODO: Test classes
class test_User(unittest.TestCase):

    def test_id(self):
        p1 = User(self)
        self.assertEquals(p1.id == 1)   # TODO: Fill in type

    def test_username(self):
        p1 = User(self)
        self.assertEquals(p1.username == "John")

    def test_password(self):
        p1 = User(self)
        self.assertEquals(p1.password == "abc123")

    def test_email(self):
        p1 = User(self)
        self.assertEquals(p1.email == "john@york.ca")

    def test_user_type_id(self):
        p1 = User(self)
        self.assertEquals(p1.user_type_id == 1) # TODO: Fill in type

    def test_user_type(self):
        p1 = User(self)
        self.assertEquals(p1.user_type == "") # TODO: Fill in type