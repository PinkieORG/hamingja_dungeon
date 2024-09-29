import unittest

import numpy as np

from areas.area import Area
from direction.direction import Direction
from utils import print_test_areas, get_test_areas, print_name


class AreaPrintTests(unittest.TestCase):
    def test_border(self):
        print("border test:")
        print_test_areas(Area.border_of_thickness)

    def test_border_in_direction(self):
        print("border in direction test:")
        for dir in Direction.get_all_directions():
            print_test_areas(Area.border_in_direction, dir)

    def test_corners_in_direction(self):
        print("corners in direction test:")
        for dir in Direction.get_all_directions():
            print_test_areas(Area.corners_in_direction, dir)

    def test_corners(self):
        print("corners test:")
        print_test_areas(Area.corners)

    def test_fit_in(self):
        to_fit = Area.from_array(np.array([[1, 1], [1, 1], [1, 1]]))
        print_test_areas(Area.fit_in, to_fit)

    def test_fit_in_anchor(self):
        to_fit = Area.from_array(np.array([[1, 0], [1, 0], [1, 1]]))
        areas = get_test_areas()
        for name, area in areas.items():
            print_name(name)
            print("original: ")
            area.print_area()
            print("border (anchor): ")
            area.border_of_thickness().print_area()
            print("result: ")
            area.fit_in(to_fit, area.border_of_thickness()).print_area()

    def test_fit_in_two_anchor(self):
        to_fit = Area.from_array(np.array([[1, 0], [1, 0], [1, 1]]))
        to_fit_anchor = Area.from_array(np.array([[0, 0], [1, 0], [1, 0]]))
        areas = get_test_areas()
        for name, area in areas.items():
            print_name(name)
            print("original: ")
            area.print_area()
            print("border (anchor): ")
            area.border_of_thickness().print_area()
            print("result: ")
            area.fit_in(to_fit, area.border_of_thickness(), to_fit_anchor).print_area()
