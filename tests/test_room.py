from unittest import TestCase

from hamingja_dungeon.areas.rooms.room import CircleRoom
from test_utils import print_dungeon_object


class TestCircleRoom(TestCase):
    circle_room = CircleRoom(15)
    print_dungeon_object(circle_room)
    circle_room.room_anchor.print()
