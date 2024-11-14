import pytest
from model import Material_Type

# TODO: Test classes
class test_Material_Type():

    def test_id(self):
        p1 = Material_Type(self)
        assert p1.id == 2

    def test_name(self):
        p1 = Material_Type(self)
        assert p1.name == "PLA"