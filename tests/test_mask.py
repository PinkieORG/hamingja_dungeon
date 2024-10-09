from __future__ import annotations
from unittest import TestCase

import numpy as np
from hamingja_dungeon.dungeon_elements.mask import Mask
from hamingja_dungeon.utils.direction import Direction
from hamingja_dungeon.utils.vector import Vector
from test_utils import print_test_areas, get_test_areas, print_name


class TestMask(TestCase):
    def test__set_array_values(self):
        mask = Mask((5,5))
        mask._set_array_values(Vector(1,1), Mask((5,5)), False)
        mask._set_array_values(Vector(6,6), Mask((5,5)), False)
        print(mask)

    def test_border(self):
        print("border test:")
        print_test_areas(Mask.border_mask)

    def test_border_in_direction(self):
        print("border in direction test:")
        for dir in Direction.get_all_directions():
            print_test_areas(Mask.border_mask, dir)

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
            print(area)
            print("border (anchor): ")
            print(area.border_mask())
            print("result: ")
            print(area.fit_in(to_fit, area.border_mask()))

    def test_fit_in_two_anchor(self):
        to_fit = Mask.from_array(np.array([[1, 0], [1, 0], [1, 1]]))
        to_fit_anchor = Mask.from_array(np.array([[0, 0], [1, 0], [1, 0]]))
        areas = get_test_areas()
        for name, area in areas.items():
            print_name(name)
            print("original: ")
            print(area)
            print("border (anchor): ")
            print(area.border_mask())
            print("result: ")
            print(area.fit_in(to_fit, area.border_mask(), to_fit_anchor))
