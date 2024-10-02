from __future__ import annotations

from typing import Tuple

import numpy as np

from hamingja_dungeon import tile_types
from hamingja_dungeon.utils.area import Area
from hamingja_dungeon.dungeon_elements.dungeon_object import DungeonObject
from hamingja_dungeon.utils.exceptions import EmptyFitArea

from hamingja_dungeon.hallway_designers.hallway_designer import HallwayDesigner
from hamingja_dungeon.utils.vector import Vector
from hamingja_dungeon.dungeon_elements.room import Room


class DungeonArea(DungeonObject):
    """Dungeon object that can hold rooms."""

    def __init__(self, size: Tuple[int, int], fill_value: np.ndarray = None):
        if fill_value is None:
            fill_value = tile_types.wall
        super().__init__(size, fill_value=fill_value)
        # self.room_graph = Graph()

    def fit_room_adjacent(self, to_fit: Room, neighbour_id: int) -> np.array:
        """Fits a room next to one already in the dungeon area. Rooms will share a
        border and will be fitted with respect to their room_anchor."""
        if neighbour_id not in self.children:
            raise ValueError(
                "The neighbour of the object to fit has to be a child of this object."
            )
        neighbour = self.get_child(neighbour_id)
        if not isinstance(neighbour.object, Room):
            raise ValueError("The neighbour of the object has to be a room.")

        anchor = Area.empty_area(self.size).insert_area(
            neighbour.origin, neighbour.object.room_anchor
        )
        without_children = (~self.child_area()).insert_area(
            neighbour.origin, neighbour.object.border()
        )
        return without_children.fit_in(
            to_fit, anchor=anchor, to_fit_anchor=to_fit.room_anchor
        )

    def add_room(self, origin: Vector, room: Room) -> int:
        """Adds a new room at the given origin. Returns its new id."""
        id = self.add_child(origin, room)
        # self.room_graph.push(id)
        return id

    def add_room_adjacent(self, room: Room, neighbour_id: int) -> int:
        """Adds a new room that will be adjacent to its given neighbour.
        They will share a wall. Returns its new id."""
        fit_area = self.fit_room_adjacent(room, neighbour_id=neighbour_id)
        if fit_area.is_empty():
            raise EmptyFitArea("The new room cannot be fitted.")
        origin = fit_area.sample()
        id = self.add_room(origin, room)
        return id

    def make_entrance(
        self, first_id: int, second_id: int, fill_value: np.ndarray = None
    ) -> None:
        """Make entrance between two already placed room given by their ids. The
        entrance will be a new child inserted into both room and will have the given
        fill value."""
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
        border_intersection = self.intersection(
            first.origin,
            first_object.connected_border(),
            second.origin,
            second_object.connected_border(),
        )
        if border_intersection.is_empty():
            raise EmptyFitArea(
                "Cannot make entrance between two rooms that do " "not share a border."
            )
        # TODO support entrances of larger size.
        entrance_point = border_intersection.sample()
        entrance = DungeonObject((1, 1), fill_value=fill_value)
        first_object.add_child(entrance_point - first.origin, entrance)
        second_object.add_child(entrance_point - second.origin, entrance)
