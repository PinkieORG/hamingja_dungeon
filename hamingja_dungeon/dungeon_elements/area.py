from __future__ import annotations

from copy import deepcopy
from typing import Tuple

import numpy as np

from hamingja_dungeon.dungeon_elements.chamber_graph import ObjectContainer
from hamingja_dungeon.dungeon_elements.mask import Mask
from hamingja_dungeon.tile_types import default
from hamingja_dungeon.utils.checks.area_checks import (
    check_value_is_tile_type,
)
from hamingja_dungeon.utils.checks.array_checks import check_array_is_same_shape
from hamingja_dungeon.utils.checks.mask_checks import (
    check_masks_are_same_size,
    check_vector_is_positive,
)
from hamingja_dungeon.utils.checks.vector_checks import check_origin_is_positive
from hamingja_dungeon.utils.utils import crop
from hamingja_dungeon.utils.vector import Vector


class Area(Mask):
    """Represent an area in the dungeon with its tile representation.
    It can have sub-areas (children)."""

    def __init__(self, size: Tuple[int, int], fill_value: np.ndarray = default):
        super().__init__(size)
        check_value_is_tile_type(fill_value)
        self._tiles = np.full(size, fill_value=fill_value)
        self.children = ObjectContainer()

    def _crop_tiles(self, origin: Vector, size: Tuple[int, int]) -> np.ndarray:
        """Returns a cropped tiles from the given origin given by the size."""
        check_vector_is_positive(origin)
        return crop(self.tiles, origin, size)

    @property
    def tiles(self) -> np.ndarray:
        return self._tiles

    @tiles.setter
    def tiles(self, tiles: np.ndarray) -> None:
        check_array_is_same_shape(self.tiles, tiles)
        check_value_is_tile_type(tiles)

    def get_children_ids(self) -> list[int]:
        return self.children.get_all_object_ids()

    def in_childless_mask(self, vector: Vector) -> bool:
        """Checks whether a point is in an area not occupied by children."""
        return self.childless_mask().is_inside_mask(vector)

    def fullness(self) -> float:
        return self.embedded_all_children_mask().volume() / self.volume()

    def embedded_child_mask(self, child_id: int) -> Mask:
        """Returns a mask of the child given by its id. The result has the same size
        as the area."""
        result = Mask.empty_mask(self.size)
        result.insert_mask(self.get_child_origin(child_id), self.get_child(child_id))
        return result

    def embedded_children_mask(self, children_ids: list[int]) -> Mask:
        """Returns a combined masks of the children given by their ids. The result has
        the same size as the area."""
        result = Mask.empty_mask(self.size)
        for child_id in children_ids:
            result |= self.embedded_child_mask(child_id)
        return result

    def embedded_all_children_mask(self) -> Mask:
        """Returns a combined masks of all the children. The result has the same size
        as the area."""
        return self.embedded_children_mask(self.get_children_ids())

    def childless_mask(self) -> Mask:
        """Returns a mask with the children removed."""
        result = Mask.from_array(self.array)
        return result & ~self.embedded_all_children_mask()

    def fill(self, value: np.ndarray) -> None:
        """Will fill the area with the given value."""
        self.tiles = np.full(self.size, value)

    def draw_on_mask(self, value: np.ndarray, mask: Mask) -> None:
        """Will fill the area with the given value with respect to the
        given mask."""
        check_masks_are_same_size(self, mask)
        check_value_is_tile_type(value)
        self.tiles[mask.array] = value

    def draw_border(self, value: np.ndarray, thickness: int = 1) -> None:
        """Will draw the border of the given thickness with the given value."""
        self.draw_on_mask(value, mask=self.border_mask(thickness))

    def draw_borderless(self, value: np.ndarray) -> None:
        """Will draw the inside with the given value."""
        self.draw_on_mask(value, mask=self.borderless_mask())

    def draw_area(self, origin: Vector, area: Area) -> None:
        """Will draw another area with respect to its mask and origin. If it protrudes
        outside of this area it will be cropped."""
        afflicted_tiles = self._crop_tiles(origin, area.size)
        new_size = (afflicted_tiles.shape[0], afflicted_tiles.shape[1])
        cropped_mask = area._crop_array(Vector(0, 0), new_size)
        cropped_tiles = area._crop_tiles(Vector(0, 0), new_size)
        afflicted_tiles[cropped_mask] = cropped_tiles[cropped_mask]

    def add_child(self, origin: Vector, area: Area) -> int:
        """Adds child to the area. Returns its new id."""
        check_origin_is_positive(origin)
        return self.children.add_object_with_data(area, data={"origin": origin})

    def remove_child(self, child_id: int) -> None:
        """Removes a child by its id."""
        self.children.remove_object(child_id)

    def get_child(self, child_id: int) -> Area:
        """Returns the child of the given id."""
        return self.children.get_object(child_id)

    def get_child_origin(self, child_id: int) -> Vector:
        return self.children.get_object_data(child_id)["origin"]

    # TODO binary search?
    def get_children_at(self, point: Vector) -> list[int]:
        """Returns ids of all children at the given point."""
        result = []
        for child_id in self.get_children_ids():
            embedded_child_mask = self.embedded_child_mask(child_id)
            if embedded_child_mask.is_inside_mask(point):
                result.append(child_id)
        return result

    def draw_children(self) -> Area:
        """Draws all of its children."""
        result = deepcopy(self)
        for child_id in self.get_children_ids():
            child = self.get_child(child_id)
            with_children = child.draw_children()
            origin = self.get_child_origin(child_id)
            result.draw_area(origin, with_children)
        return result

    # TODO Support borders of thickness larger than 1.
    def fit_adjacent_at_border(self, to_fit: Area, neighbour_id: int) -> Mask:
        """Fits the new area next to already added child given by its id.
        The new area will share a border with the neighbour."""
        neighbour = self.get_child(neighbour_id)
        neighbour_origin = self.get_child_origin(neighbour_id)
        embedded_neighbour_border = Mask.empty_mask(self.size)
        embedded_neighbour_border.insert_mask(neighbour_origin, neighbour.border_mask())
        border_without_children = self.childless_mask() | embedded_neighbour_border
        return border_without_children.fit_in_anchors_touching(
            to_fit, anchor=embedded_neighbour_border, to_fit_anchor=to_fit.border_mask()
        )
