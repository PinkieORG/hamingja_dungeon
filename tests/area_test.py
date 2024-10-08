import unittest

import numpy as np

from hamingja_dungeon.dungeon_elements.mask import Mask
from hamingja_dungeon.utils.direction import Direction
from test_utils import print_test_areas, get_test_areas, print_name


class AreaPrintTests(unittest.TestCase):
    def test_border(self):
        print("border test:")
        print_test_areas(Mask.border)

    def test_border_in_direction(self):
        print("border in direction test:")
        for dir in Direction.get_all_directions():
            print_test_areas(Mask.border, dir)

    def test_corners_in_direction(self):
        print("corners in direction test:")
        for dir in Direction.get_all_directions():
            print_test_areas(Mask.corners_in_direction, dir)

    def test_corners(self):
        print("corners test:")
        print_test_areas(Mask.corners)

    def test_outside_corners(self):
        print("corners test:")
        print_test_areas(Mask.outside_corners)

    def test_fit_in(self):
        to_fit = Mask.from_array(np.array([[1, 1], [1, 1], [1, 1]]))
        print_test_areas(Mask.fit_in, to_fit)

    def test_fit_in_anchor(self):
        to_fit = Mask.from_array(np.array([[1, 0], [1, 0], [1, 1]]))
        areas = get_test_areas()
        for name, area in areas.items():
            print_name(name)
            print("original: ")
            area.print()
            print("border (anchor): ")
            area.border().print()
            print("result: ")
            area.fit_in(to_fit, area.border()).print()

    def test_fit_in_two_anchor(self):
        to_fit = Mask.from_array(np.array([[1, 0], [1, 0], [1, 1]]))
        to_fit_anchor = Mask.from_array(np.array([[0, 0], [1, 0], [1, 0]]))
        areas = get_test_areas()
        for name, area in areas.items():
            print_name(name)
            print("original: ")
            area.print()
            print("border (anchor): ")
            area.border().print()
            print("result: ")
            area.fit_in(to_fit, area.border(), to_fit_anchor).print()
