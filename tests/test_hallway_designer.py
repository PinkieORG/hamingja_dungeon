from unittest import TestCase

from hamingja_dungeon.areas.rooms.hallways.hallway_designer import HallwayDesigner
from hamingja_dungeon.areas.rooms.room import Room
from hamingja_dungeon.areas.vector import Vector
from hamingja_dungeon.direction.direction import Direction
from test_utils import (
    get_test_dungeon_area,
    print_dungeon_object,
)


class TestHallwayDesigner(TestCase):
    def test_t(self):
        dungeon_area = get_test_dungeon_area()

        dungeon_area.add_room(Vector(2, 1), Room((4, 4)))
        dungeon_area.add_room(Vector(6, 9), Room((6, 6)))

        designer = HallwayDesigner(dungeon_area)
        origin, hallway = designer.design_hallway(Vector(4, 5), [Direction.EAST])

        dungeon_area.add_room(origin, hallway)
        print_dungeon_object(dungeon_area)
