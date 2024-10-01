from __future__ import annotations

import itertools
from dataclasses import dataclass
from typing import Tuple

import numpy as np

from hamingja_dungeon.areas.area import Area
from hamingja_dungeon.areas.vector import Vector
from hamingja_dungeon.tile_types import default, tile_dt


@dataclass
class Child:
    origin: Vector
    object: DungeonObject


class DungeonObject(Area):
    """Represent an object in the dungeon. It can have sub-objects
    (children)."""

    def __init__(self, size: Tuple[int, int], fill_value: np.ndarray = None):
        super().__init__(size)
        if fill_value is None:
            fill_value = default

        self._tiles = np.full(size, fill_value=fill_value)
        self.children: dict[int, Child] = {}
        self.id_generator = itertools.count()

    @property
    def tiles(self) -> np.ndarray:
        return self._tiles

    def in_childless_area(self, p: Vector) -> bool:
        return self.childless_area().is_inside_area(p)

    def fullness(self) -> float:
        return self.child_area().volume() / self.volume()

    def child_area(self) -> Area:
        """Returns a combined area of the children."""
        result = Area.empty_area(self.size)
        for child in self.children.values():
            origin = child.origin
            object = child.object
            afflicted_area = result.mask[
                origin.y : origin.y + object.h, origin.x : origin.x + object.w
            ]

            afflicted_area[object.mask] = True
        return result

    def childless_area(self) -> Area:
        """Returns an area with the children removed."""
        result = Area.from_array(self.mask)
        return result & ~self.child_area()

    def inner_area(self) -> Area:
        """Returns an area without the border."""
        return Area.from_array(self.mask) - self.border()

    def draw(self, value: np.ndarray, mask: Area = None) -> None:
        """Will draw on the object with the given value with respect to the
        given mask. If no mask is given will draw everywhere."""
        if mask is None:
            mask = Area(self.size)
        if value.dtype != tile_dt:
            raise ValueError("Fill value has to have the tile dtype.")
        if mask.size != self.size:
            raise ValueError("The mask has to have the the size of the object.")
        self.tiles[mask.mask] = value

    def draw_border(self, value: np.ndarray, thickness: int = 1) -> None:
        """Will draw the border of the given thickness with the given value."""
        if value.dtype != tile_dt:
            raise ValueError("fill_value needs to have the tile dtype.")
        self.draw(value, mask=self.border(thickness))

    def draw_inside(self, value: np.ndarray):
        """Will draw the inside with the given value."""
        if value.dtype != tile_dt:
            raise ValueError("fill_value needs to have the tile dtype.")
        self.draw(value, mask=self.inner_area())

    def draw_dungeon_object(self, p: Vector, dungeon_object: DungeonObject) -> None:
        """Will draw another dungeon object with respect to its mask. If it
        protrudes outside of this objects area it will be cropped."""
        if not p.is_positive():
            raise ValueError("The dungeon object cannot be drawn from negative point.")
        afflicted_tiles = self.tiles[
            p.y : p.y + dungeon_object.h, p.x : p.x + dungeon_object.w
        ]
        if 0 in afflicted_tiles.shape:
            return
        cropped_mask = dungeon_object.mask[
            0 : afflicted_tiles.shape[0], 0 : afflicted_tiles.shape[1]
        ]
        cropped_tiles = dungeon_object.tiles[
            0 : afflicted_tiles.shape[0], 0 : afflicted_tiles.shape[1]
        ]
        afflicted_tiles[cropped_mask] = cropped_tiles[cropped_mask]

    def add_child(self, origin: Vector, dungeon_object: DungeonObject) -> int:
        """Adds child to the object. Returns its new id."""
        if not origin.is_positive():
            raise ValueError("The origin of the new child has to be positive.")
        id = next(self.id_generator)
        self.children[id] = Child(origin, dungeon_object)
        return id

    def get_child(self, id: int) -> Child:
        """Returns the child of the given id."""
        if id not in self.children:
            raise ValueError("The child of this id does not exists.")
        return self.children.get(id)

    def draw_children(self) -> None:
        """Draws all of its children."""
        for child in self.children.values():
            child.object.draw_children()
            self.draw_dungeon_object(child.origin, child.object)

    def fit_adjacent_at_border(self, to_fit: DungeonObject, neighbour_id: int) -> Area:
        """Fits the new area next to already added child given by its id.
        The new object will share a border with the neighbour."""

        # TODO Support borders of thickness larger than 1.

        if neighbour_id not in self.children:
            raise ValueError(
                "The neighbour of the object to fit has to be a "
                "child of this object."
            )
        neighbour = self.get_child(neighbour_id)

        anchor = Area.empty_area(self.size).insert_area(
            neighbour.origin, neighbour.object.border()
        )
        without_children = self.childless_area().insert_area(
            neighbour.origin, neighbour.object.border()
        )
        return without_children.fit_in(
            to_fit, anchor=anchor, to_fit_anchor=to_fit.border()
        )
