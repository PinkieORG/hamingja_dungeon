from typing import Tuple

import numpy as np

import tile_types
from areas.dungeon_object import DungeonObject
from areas.exceptions import EmptyFitArea
from areas.point import Point
from areas.rooms.room import Room


class DungeonArea(DungeonObject):
    """Dungeon object that can hold rooms."""
    def __init__(self, size: Tuple[int, int], fill_value: np.ndarray = None):
        if fill_value is None:
            fill_value = tile_types.wall
        super().__init__(size, fill_value=fill_value)
        # self.room_graph = Graph()

    def add_room(self, origin: Point, room: Room) -> int:
        """Adds a new room at the given origin. Returns its new id."""
        id = self.add_child(origin, room)
        # self.room_graph.push(id)
        return id

    def add_room_adjacent(self, room: Room, neighbour_id: int) -> int:
        """Adds a new room that will be adjacent to its given neighbour.
        They will share a wall. Returns its new id."""
        fit_area = self.fit_adjacent_at_border(room, neighbour_id=neighbour_id)
        if fit_area.is_empty():
            raise EmptyFitArea("The new room cannot be fitted.")
        origin = fit_area.sample()
        id = self.add_room(origin, room)
        return id

    def make_entrance(self, first_id: int, second_id: int,
                      fill_value: np.ndarray = None) -> None:
        if fill_value is None:
            fill_value = tile_types.floor
        if fill_value.dtype != tile_types.tile_dt:
            raise ValueError("Fill value has to have the tile dtype.")
        if first_id not in self.children or second_id not in self.children:
            raise ValueError("Rooms not in children.")
        first = self.get_child(first_id)
        first_object = first.object
        second = self.get_child(second_id)
        second_object = second.object
        border_intersection = self.intersection(first.origin,
                                                first_object.connected_border(),
                                                second.origin,
                                                second_object.connected_border())
        if border_intersection.is_empty():
            raise EmptyFitArea("Cannot make entrance between two rooms that do "
                               "not share a border.")
        # TODO support entrances of larger size.
        entrance_point = border_intersection.sample()
        entrance = DungeonObject((1, 1), fill_value=fill_value)
        first_object.add_child(entrance_point - first.origin, entrance)
        second_object.add_child(entrance_point - second.origin, entrance)
