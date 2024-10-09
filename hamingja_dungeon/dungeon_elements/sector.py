from __future__ import annotations

from typing import Tuple

import igraph as ig
import numpy as np

from hamingja_dungeon import tile_types
from hamingja_dungeon.dungeon_elements.area import Area, AreaWithOrigin
from hamingja_dungeon.dungeon_elements.chamber import Chamber
from hamingja_dungeon.dungeon_elements.mask import Mask
from hamingja_dungeon.utils.checks.area_checks import check_child_of_id_exists
from hamingja_dungeon.utils.checks.sector_checks import check_area_is_room
from hamingja_dungeon.utils.exceptions import EmptyFitArea
from hamingja_dungeon.utils.vector import Vector


class Sector(Area):
    """Area that can hold rooms."""

    def __init__(self, size: Tuple[int, int], fill_value: np.ndarray = None):
        if fill_value is None:
            fill_value = tile_types.wall
        super().__init__(size, fill_value=fill_value)
        self.room_graph = ig.Graph()

    def get_chambers(self) -> dict[int, AreaWithOrigin]:
        result = {}
        for room_id, child in self.children.items():
            if isinstance(child.area, Chamber):
                result[room_id] = child
        return result

    def fit_room_adjacent(self, to_fit: Chamber, neighbour_id: int) -> Mask:
        """Fits a room next to one already in the sector. Rooms will share a
        border and will be fitted with respect to their entrance points."""
        check_child_of_id_exists(neighbour_id, self.children)
        neighbour = self.get_child(neighbour_id)
        check_area_is_room(neighbour.area)
        embedded_entrypoints = Mask.empty_mask(self.size).insert_mask(
            neighbour.origin, neighbour.area.entrypoints
        )
        border_without_children = self.childless_mask().insert_mask(
            neighbour.origin, neighbour.area.border_mask()
        )
        return border_without_children.fit_in_anchors_touching(
            to_fit, anchor=embedded_entrypoints, to_fit_anchor=to_fit.entrypoints
        )

    def add_room(self, origin: Vector, room: Chamber) -> int:
        """Adds a new room at the given origin. Returns its new id."""
        new_id = self.add_child(origin, room)
        self.room_graph.add_vertex(id=new_id)
        return new_id

    def remove_room(self, to_remove_id: int) -> None:
        to_remove_index = self.room_graph.vs.find(id=to_remove_id)
        edge_indexes = self.room_graph.incident(to_remove_index)
        for index in edge_indexes:
            edge = self.room_graph.es[index]
            entrance_ids = edge["ids"]
            for room_id, entrance_id in entrance_ids.items():
                self.get_child(room_id).area.remove_entrance(entrance_id)
        self.room_graph.delete_vertices([to_remove_index])
        self.remove_child(to_remove_id)

    def add_room_adjacent(self, room: Chamber, neighbour_id: int) -> int:
        """Adds a new room that will be adjacent to its given neighbour.
        They will share a wall. Returns its new id."""
        fit_area = self.fit_room_adjacent(room, neighbour_id=neighbour_id)
        if fit_area.is_empty():
            raise EmptyFitArea("The new room cannot be fitted.")
        origin = fit_area.sample_mask_coordinate()
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
        first_room = first.area
        second = self.get_child(second_id)
        second_room = second.area
        if not isinstance(first_room, Chamber) or not isinstance(second_room, Chamber):
            raise ValueError("Can make entrances only between rooms.")

        border_intersection = self.intersection(
            first.origin,
            first_room.entrypoints,
            second.origin,
            second_room.entrypoints,
        )
        if border_intersection.is_empty():
            raise EmptyFitArea(
                "Cannot make entrance between two rooms that do not share a border."
            )
        # TODO support entrances of larger size.
        entrance_point = border_intersection.sample_mask_coordinate()
        entrance = Area((1, 1), fill_value=fill_value)
        first_entrance_id = first_room.place_entrance(
            entrance_point - first.origin, entrance
        )
        second_entrance_id = second_room.place_entrance(
            entrance_point - second.origin, entrance
        )

        first_index = self.room_graph.vs.find(id=first_id).index
        second_index = self.room_graph.vs.find(id=second_id).index

        self.room_graph.add_edge(
            first_index,
            second_index,
            ids={first_id: first_entrance_id, second_id: second_entrance_id},
        )
