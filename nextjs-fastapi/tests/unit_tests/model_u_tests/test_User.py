import pytest
from model import User

# TODO: Test classes
class test_User():

    def test_id(self):
        p1 = User(self)
        assert p1.id == 1

    def test_username(self):
        p1 = User(self)
        assert p1.username == "John"

    def test_password(self):
        p1 = User(self)
        assert p1.password == "abc123"

    def test_email(self):
        p1 = User(self)
        assert p1.email == "john@p3d.ca"

    def test_user_type_id(self):
        p1 = User(self)
        assert p1.user_type_id == 1

    def test_user_type(self):
        p1 = User(self)
        assert p1.user_type == "Admin"