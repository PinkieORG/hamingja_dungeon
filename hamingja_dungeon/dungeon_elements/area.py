from __future__ import annotations

import itertools
from dataclasses import dataclass
from typing import Tuple

import numpy as np

from hamingja_dungeon.dungeon_elements.shape import Shape
from hamingja_dungeon.utils.vector import Vector
from hamingja_dungeon.tile_types import default, tile_dt


@dataclass
class Child:
    origin: Vector
    object: Area


class Area(Shape):
    """Represent an area in the dungeon with its tile representation.
    It can have sub-areas (children)."""

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
        """Checks whether a point is in an area not occupied by children."""
        return self.childless_shape().is_inside_mask(p)

    def fullness(self) -> float:
        return self.children_shapes().volume() / self.volume()

    def child_shape(self, id: int) -> Shape:
        """Returns a shape of the child given by its id. The result has the same size
        as the area."""
        result = Shape.empty(self.size)
        child = self.get_child(id)
        origin = child.origin
        object = child.object
        afflicted_area = result.mask[
                         origin.y: origin.y + object.h, origin.x: origin.x + object.w
                         ]

        afflicted_area[object.mask] = True
        return result

    def children_shapes(self, without: [int] = None) -> Shape:
        """Returns a combined shapes of the children."""
        if without is None:
            without = []
        result = Shape.empty(self.size)
        children = {
            key: value for key, value in self.children.items() if key not in without
        }
        for child in children.values():
            origin = child.origin
            object = child.object
            afflicted_area = result.mask[
                origin.y : origin.y + object.h, origin.x : origin.x + object.w
            ]

            afflicted_area[object.mask] = True
        return result

    def childless_shape(self) -> Shape:
        """Returns a shape with the children removed."""
        result = Shape.from_array(self.mask)
        return result & ~self.children_shapes()

    def inner_shape(self) -> Shape:
        """Returns a shape without the border."""
        return Shape.from_array(self.mask) - self.border()

    def draw(self, value: np.ndarray, mask: Shape = None) -> None:
        """Will draw on the area with the given value with respect to the
        given mask. If no mask is given will draw everywhere."""
        if mask is None:
            mask = Shape(self.size)
        if value.dtype != tile_dt:
            raise ValueError("Fill value has to have the tile dtype.")
        if mask.size != self.size:
            raise ValueError("The mask has to have the the size of the area.")
        self.tiles[mask.mask] = value

    def draw_border(self, value: np.ndarray, thickness: int = 1) -> None:
        """Will draw the border of the given thickness with the given value."""
        if value.dtype != tile_dt:
            raise ValueError("fill_value needs to have the tile dtype.")
        self.draw(value, mask=self.border(thickness))

    def draw_inside(self, value: np.ndarray) -> None:
        """Will draw the inside with the given value."""
        if value.dtype != tile_dt:
            raise ValueError("fill_value needs to have the tile dtype.")
        self.draw(value, mask=self.inner_shape())

    def draw_area(self, p: Vector, area: Area) -> None:
        """Will draw another area with respect to its mask. If it
        protrudes outside of this area it will be cropped."""
        if not p.is_positive():
            raise ValueError("The area cannot be drawn from negative point.")
        afflicted_tiles = self.tiles[p.y : p.y + area.h, p.x : p.x + area.w]
        if 0 in afflicted_tiles.shape:
            return
        cropped_mask = area.mask[
            0 : afflicted_tiles.shape[0], 0 : afflicted_tiles.shape[1]
        ]
        cropped_tiles = area.tiles[
            0 : afflicted_tiles.shape[0], 0 : afflicted_tiles.shape[1]
        ]
        afflicted_tiles[cropped_mask] = cropped_tiles[cropped_mask]

    def add_child(self, origin: Vector, area: Area) -> int:
        """Adds child to the area. Returns its new id."""
        if not origin.is_positive():
            raise ValueError("The origin of the new child has to be positive.")
        id = next(self.id_generator)
        self.children[id] = Child(origin, area)
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
            self.draw_area(child.origin, child.object)

    def fit_adjacent_at_border(self, to_fit: Area, neighbour_id: int) -> Shape:
        """Fits the new area next to already added child given by its id.
        The new area will share a border with the neighbour."""

        # TODO Support borders of thickness larger than 1.

        if neighbour_id not in self.children:
            raise ValueError(
                "The neighbour of the area to fit has to be a child of this area."
            )
        neighbour = self.get_child(neighbour_id)

        anchor = Shape.empty(self.size).insert_shape(
            neighbour.origin, neighbour.object.border()
        )
        without_children = self.childless_shape().insert_shape(
            neighbour.origin, neighbour.object.border()
        )
        return without_children.fit_in(
            to_fit, anchor=anchor, to_fit_anchor=to_fit.border()
        )
