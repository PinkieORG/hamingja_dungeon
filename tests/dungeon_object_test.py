import unittest

import numpy as np
from scipy.ndimage import binary_dilation

from areas.dungeon_object import DungeonObject
from areas.point import Point
from tile_types import wall, carpet, column
from test_utils import (
    get_test_dungeon_objects,
    print_name,
    print_dungeon_object,
    print_test_dungeon_objects,
)


class PrintTests(unittest.TestCase):
    def test_draw_border(self):
        dungeon_objects = get_test_dungeon_objects()
        for name, dungeon_object in dungeon_objects.items():
            print_name(name)
            print("original: ")
            print_dungeon_object(dungeon_object)
            print("result: ")
            dungeon_object.border_thickness = 2
            dungeon_object.draw_border(wall)
            print_dungeon_object(dungeon_object)

    def test_draw_inside(self):
        dungeon_objects = get_test_dungeon_objects()
        for name, dungeon_object in dungeon_objects.items():
            print_name(name)
            print("original: ")
            print_dungeon_object(dungeon_object)
            print("result: ")
            dungeon_object.border_thickness = 1
            dungeon_object.draw_inside(carpet)
            print_dungeon_object(dungeon_object)

    def test_draw_children(self):
        to_add = DungeonObject((3, 2), fill_value=carpet)
        print_test_dungeon_objects(DungeonObject.add_child, Point(4, 7), to_add)

    def test_fit_adjacent_at_border(self):
        neighbour = DungeonObject((5, 3), fill_value=carpet, border_thickness=1)
        to_fit = DungeonObject((3, 3), fill_value=column, border_thickness=1)
        l_shape = get_test_dungeon_objects().get("L shape")
        id = l_shape.add_child(Point(1, 2), neighbour)
        print("original: ")
        print_dungeon_object(l_shape)
        result = l_shape.fit_adjacent_at_border(to_fit, id)
        print("result: ")
        result.print()

    def test(self):
        corner = np.array([[1, 0], [1, 1]])

        structure = np.array([[1, 1], [1, 1]])
        corner = np.pad(corner, ((5, 0), (5, 0)), constant_values=0)
        print(corner)
        print(binary_dilation(corner, structure=structure, iterations=3).astype(int))
