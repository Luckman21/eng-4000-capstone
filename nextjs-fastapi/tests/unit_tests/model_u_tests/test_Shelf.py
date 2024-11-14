import pytest
from Shelf.py import Shelf

# TODO: Test classes
class test_Shelf():

    def test_id(self):
        p1 = Shelf(self)
        assert p1.id == 1

    def test_humid(self):
        p1 = Shelf(self)
        assert p1.humidity_pct == 20

    def test_temp(self):
        p1 = Shelf(self)
        assert p1.temperature_cel == 10