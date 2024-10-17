from __future__ import annotations
from typing import Tuple
import numpy as np
from hamingja_dungeon import tile_types
from hamingja_dungeon.dungeon_elements.area import Area
from hamingja_dungeon.dungeon_elements.chamber import Chamber
from hamingja_dungeon.dungeon_elements.mask import Mask
from hamingja_dungeon.utils.checks.sector_checks import check_chamber_of_id_exists
from hamingja_dungeon.utils.exceptions import EmptyFitArea
from hamingja_dungeon.utils.vector import Vector


class Sector(Area):
    """Area that can hold chambers."""

    def __init__(self, size: Tuple[int, int], fill_value: np.ndarray = tile_types.wall):
        super().__init__(size, fill_value=fill_value)
        self.chamber_ids: list[int] = []

    def _remove_chamber_entrance(self, chamber_id: int, entrance_id: int) -> None:
        chamber = self.get_child(chamber_id)
        chamber.remove_chamber(entrance_id)

    def _connect_chambers(
        self,
        chamber_id_1: int,
        chamber_id_2: int,
        entrance_id_1: int,
        entrance_id_2: int,
    ) -> None:
        data = {
            "entrance_ids": {
                chamber_id_1: entrance_id_1,
                chamber_id_2: entrance_id_2,
            }
        }
        self.children.add_connection_with_data(chamber_id_1, chamber_id_2, data)

    def _remove_entrances_from_neighbours(self, chamber_id: int) -> None:
        for neighbour_id in self.children.get_connected_objects(chamber_id):
            connection_data = self.children.get_connection_data(
                chamber_id, neighbour_id
            )
            neighbour_entrance_id = connection_data["entrance_ids"][neighbour_id]
            self._remove_chamber_entrance(neighbour_id, neighbour_entrance_id)

    def _get_entrance_point(
        self, chamber_1: Chamber, chamber_2: Chamber, origin_1: Vector, origin_2: Vector
    ) -> Vector:
        border_intersection = self.intersection(
            origin_1,
            chamber_1.entrypoints,
            origin_2,
            chamber_2.entrypoints,
        )
        if border_intersection.is_empty():
            raise EmptyFitArea(
                "Cannot make entrance between two rooms that do not share a border."
            )
        entrance_point = border_intersection.sample_mask_coordinate()
        return entrance_point

    def add_chamber(self, origin: Vector, chamber: Chamber) -> int:
        """Adds a new room at the given origin. Returns its new id."""
        new_id = self.add_child(origin, chamber)
        self.chamber_ids.append(new_id)
        return new_id

    def get_chamber(self, chamber_id: int) -> Chamber:
        check_chamber_of_id_exists(chamber_id, self.chamber_ids)
        return self.get_child(chamber_id)

    def remove_chamber(self, to_remove_id: int) -> None:
        self._remove_entrances_from_neighbours(to_remove_id)
        self.remove_child(to_remove_id)

    def fit_chamber_adjacent(self, to_fit: Chamber, neighbour_id: int) -> Mask:
        """Fits a chamber next to one already in the sector. Rooms will share a
        border and will be fitted with respect to their entrance points."""
        neighbour = self.get_chamber(neighbour_id)
        origin = self.get_child_origin(neighbour_id)
        embedded_entrypoints = Mask.empty_mask(self.size).insert_mask(
            origin, neighbour.entrypoints
        )
        border_without_children = self.childless_mask().insert_mask(
            origin, neighbour.border_mask()
        )
        return border_without_children.fit_in_anchors_touching(
            to_fit, anchor=embedded_entrypoints, to_fit_anchor=to_fit.entrypoints
        )

    def add_room_adjacent(self, room: Chamber, neighbour_id: int) -> int:
        """Adds a new chamber that will be adjacent to its given neighbour.
        They will share a wall. Returns its new id."""
        fit_area = self.fit_chamber_adjacent(room, neighbour_id=neighbour_id)
        if fit_area.is_empty():
            raise EmptyFitArea("The new room cannot be fitted.")
        origin = fit_area.sample_mask_coordinate()
        id = self.add_chamber(origin, room)
        return id

    # TODO support entrances of larger size.
    def make_entrance_between(
        self,
        chamber_id_1: int,
        chamber_id_2: int,
        fill_value: np.ndarray = tile_types.floor,
    ) -> None:
        """Make entrance between two already placed room given by their ids. The
        entrance will be a new child inserted into both room and will have the given
        fill value."""
        chamber_1 = self.get_chamber(chamber_id_1)
        origin_1 = self.get_child_origin(chamber_id_1)
        chamber_2 = self.get_chamber(chamber_id_2)
        origin_2 = self.get_child_origin(chamber_id_2)
        entrance_point = self._get_entrance_point(
            chamber_1, chamber_2, origin_1, origin_2
        )
        entrance = Area((1, 1), fill_value=fill_value)
        entrance_id_1 = chamber_1.place_entrance(entrance_point - origin_1, entrance)
        entrance_id_2 = chamber_2.place_entrance(entrance_point - origin_2, entrance)
        self._connect_chambers(chamber_id_1, chamber_id_2, entrance_id_1, entrance_id_2)
