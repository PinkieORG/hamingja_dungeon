from unittest import TestCase

from hamingja_dungeon.areas.rooms.hallways.hallway_designer import HallwayDesigner
from hamingja_dungeon.areas.vector import Vector
from hamingja_dungeon.direction.direction import Direction
from test_utils import get_test_dungeon_objects, print_dungeon_object


class TestHallwayDesigner(TestCase):
    def test_t(self):
        dungeon_area = get_test_dungeon_objects().get("C shape")
        designer = HallwayDesigner()
        origin, hallway = designer.design_hallway(
            dungeon_area, Vector(2, 2), [Direction.EAST]
        )
        dungeon_area.draw_dungeon_object(origin, hallway)
        print_dungeon_object(dungeon_area)
