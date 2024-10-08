from unittest import TestCase

from hamingja_dungeon.dungeon_elements.room import Room
from hamingja_dungeon.utils.vector import Vector
from test_utils import get_test_sector, print_sector


class TestSector(TestCase):
    def test_make_entrance(self):
        sector = get_test_sector()
        room1 = Room((5,5))
        rid1 = sector.add_room(Vector(1,1), room1)
        print_sector(sector)
        room2 = Room((5,7))
        rid2 = sector.add_room_adjacent(room2, rid1)
        sector.make_entrance(rid1, rid2)
        print_sector(sector)

    def test_remove_room(self):
        sector = get_test_sector()
        room1 = Room((5,5))
        rid1 = sector.add_room(Vector(1,1), room1)
        room2 = Room((5,7))
        rid2 = sector.add_room(Vector(5,1),room2)
        sector.make_entrance(rid1, rid2)

        room3 = Room((4,6))
        rid3 = sector.add_room(Vector(1,5),room3)
        sector.make_entrance(rid1, rid3)

        print_sector(sector)
        sector.remove_room(rid2)
        sector.remove_room(rid3)
        print_sector(sector)
