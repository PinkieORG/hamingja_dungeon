import unittest

from hamingja_dungeon.utils.morphology.morphology import prune
from test_utils import c_shape


class PrintTests(unittest.TestCase):
    def test_prune(self):
        border = c_shape.connected_border()
        print("original: ")
        border.print()
        print("result: ")
        border.array = prune(border.array, iterations=2)
        border.print()
