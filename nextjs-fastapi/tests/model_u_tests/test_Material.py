import pytest
from model import Material

# TODO: Test classes
class test_Material():

    def test_id(self):
        p1 = Material(self)
        assert p1.id == 1

    def test_colour(self):
        p1 = Material(self)
        assert p1.colour == "Red"

    def test_name(self):
        p1 = Material(self)
        assert p1.name == "Sunset"

    def test_mass(self):
        p1 = Material(self)
        assert p1.mass == 72.6