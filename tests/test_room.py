from unittest import TestCase

from hamingja_dungeon.dungeon_elements.rectangleroom import CircleRoom
from test_utils import print_sector


class TestCircleRoom(TestCase):
    circle_room = CircleRoom(15)
    print_sector(circle_room)
    circle_room.room_anchor.print()
