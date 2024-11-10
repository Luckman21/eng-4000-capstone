import pytest
from User_Type.py import User_Type

# TODO: Test classes
class test_User_Type():

    def test_id(self):
        p1 = User_Type(self)
        assert p1.id == 1

    def test_typename(self):
        p1 = User_Type(self)
        assert p1.user_type == "Admin"