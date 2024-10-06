from unittest import TestCase
from hamingja_dungeon.hallway_designers.hallway_designer import (
    DesignerError,
    HallwayDesigner,
)
from hamingja_dungeon.dungeon_elements.room import Room
from hamingja_dungeon.utils.vector import Vector
from hamingja_dungeon.utils.direction import Direction
from test_utils import (
    get_test_sector,
    print_sector,
)


class TestHallwayDesigner(TestCase):
    def test_normal(self):
        dungeon_area = get_test_sector()

        dungeon_area.add_room(Vector(2, 1), Room((4, 4)))
        dungeon_area.add_room(Vector(6, 9), Room((6, 6)))

        designer = HallwayDesigner(dungeon_area)
        origin, hallway = designer.design_hallway(Vector(4, 4), [Direction.EAST])

        dungeon_area.add_room(origin, hallway)
        print_sector(dungeon_area)

    def test_close_rooms(self):
        dungeon_area = get_test_sector()

        id_1 = dungeon_area.add_room(Vector(2, 1), Room((4, 4)))
        id_2 = dungeon_area.add_room(Vector(2, 6), Room((6, 6)))

        designer = HallwayDesigner(dungeon_area)
        origin, hallway = designer.design_hallway(Vector(4, 4), [Direction.EAST])

        hallway_id = dungeon_area.add_room(origin, hallway)
        dungeon_area.make_entrance(id_1, hallway_id)
        print_sector(dungeon_area)

    def test_neighbour_too_close(self):
        dungeon_area = get_test_sector()

        dungeon_area.add_room(Vector(2, 1), Room((4, 4)))
        dungeon_area.add_room(Vector(2, 5), Room((6, 6)))

        designer = HallwayDesigner(dungeon_area)

        self.assertRaises(
            DesignerError, designer.design_hallway, Vector(4, 4), [Direction.EAST]
        )

    def test_close_to_wall(self):
        dungeon_area = get_test_sector()

        dungeon_area.add_room(Vector(2, 2), Room((4, 4)))

        designer = HallwayDesigner(dungeon_area)
        print_sector(dungeon_area)

        self.assertRaises(
            DesignerError, designer.design_hallway, Vector(4, 2), [Direction.WEST]
        )

    def test_closer_to_wall(self):
        dungeon_area = get_test_sector()

        dungeon_area.add_room(Vector(2, 1), Room((4, 4)))

        designer = HallwayDesigner(dungeon_area)

        self.assertRaises(
            DesignerError, designer.design_hallway, Vector(4, 1), [Direction.WEST]
        )
