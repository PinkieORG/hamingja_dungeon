from unittest import TestCase

import numpy as np

from hamingja_dungeon.dungeon_elements.hallway import Hallway
from hamingja_dungeon.dungeon_elements.rectangleroom import Chamber
from hamingja_dungeon.utils.vector import Vector
from test_utils import get_test_sector, print_sector, snake_np


class TestHallway(TestCase):
    def test_has_dead_end(self):
        hallway = Hallway(snake_np)
        print_sector(hallway)
        sector = get_test_sector()
        room1 = Chamber((5, 7))
        rid1 = sector.add_room(Vector(1, 1), room1)
        room2 = Chamber((5, 7))
        rid2 = sector.add_room(Vector(5, 1), room2)

        rid3 = sector.add_room(Vector(1, 7), hallway)
        sector.make_entrance(rid1, rid3)
        print_sector(sector)
        assert hallway.has_dead_end()
        print_sector(sector)

        sector.make_entrance(rid2, rid3)
        assert not hallway.has_dead_end()
