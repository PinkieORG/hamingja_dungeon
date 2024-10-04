from __future__ import annotations

import random
from copy import deepcopy
from typing import Tuple

import numpy as np
from scipy.ndimage import binary_erosion, binary_hit_or_miss, binary_dilation

from hamingja_dungeon.utils.morphology.structure_elements import (
    OUTSIDE_CORNERS,
    SQUARE,
    HORIZONTAL,
    VERTICAL,
    INSIDE_CORNERS,
)
from hamingja_dungeon.utils.vector import Vector
from hamingja_dungeon.utils.direction import Direction


class Shape:
    """Represents a binary area."""

    def __init__(self, size: Tuple[int, int]):
        if size[0] <= 0 or size[1] <= 0:
            raise ValueError("The size has to be positive.")
        self._mask = np.full(size, fill_value=True, dtype=np.bool)

    def _set_mask_values(self, origin: Vector, shape: Shape, set_to: bool) -> None:
        """Sets values defined by the true values of the new mask inserted to
        the given origin."""
        if not origin.is_positive():
            raise ValueError("The origin of the shape has to be positive.")
        afflicted_area = self.mask[
            origin.y : origin.y + shape.h, origin.x : origin.x + shape.w
        ]
        if 0 in afflicted_area.shape:
            return
        cropped_mask = shape.mask[
            0 : afflicted_area.shape[0], 0 : afflicted_area.shape[1]
        ]
        afflicted_area[cropped_mask] = set_to

    @staticmethod
    def from_array(in_array: np.ndarray) -> Shape:
        """Creates a new shape from a numpy array."""
        mask = np.array(in_array, dtype=bool)
        if mask.ndim != 2:
            raise ValueError("The given array has to be 2 dimensional.")
        result = Shape((mask.shape[0], mask.shape[1]))
        result.mask = mask
        return result

    @staticmethod
    def empty(size: Tuple[int, int]) -> Shape:
        """Creates an empty shape of the given size."""
        shape = Shape(size)
        shape.mask.fill(False)
        return shape

    @property
    def size(self) -> Tuple[int, int]:
        return self.h, self.w

    @property
    def h(self) -> int:
        return self.mask.shape[0]

    @property
    def w(self) -> int:
        return self.mask.shape[1]

    @property
    def mask(self) -> np.ndarray:
        return self._mask

    @mask.setter
    def mask(self, new_array: np.array) -> None:
        if new_array.ndim != 2:
            raise ValueError("The given array has to be 2 dimensional.")
        if self.mask.shape != new_array.shape:
            raise ValueError("The given array has to have a same shape.")
        if self.mask.dtype != new_array.dtype:
            raise ValueError("New array needs to have a bool dtype.")
        self._mask = new_array

    def __str__(self) -> str:
        return str(self.mask)

    def __and__(self, other: Shape) -> Shape:
        if self.size != other.size:
            raise ValueError("Shapes need to have the same sizes.")
        return Shape.from_array(self.mask & other.mask)

    def __iand__(self, other: Shape) -> Shape:
        if self.size != other.size:
            raise ValueError("Shapes need to have the same sizes.")
        self.mask &= other.mask
        return self

    def __or__(self, other: Shape) -> Shape:
        if self.size != other.size:
            raise ValueError("Shapes need to have the same sizes.")
        return Shape.from_array(self.mask | other.mask)

    def __ior__(self, other: Shape) -> Shape:
        if self.size != other.size:
            raise ValueError("Shapes need to have the same sizes.")
        self.mask |= other.mask
        return self

    def __xor__(self, other: Shape) -> Shape:
        if self.size != other.size:
            raise ValueError("Shapes need to have the same sizes.")
        return Shape.from_array(self.mask ^ other.mask)

    def __ixor__(self, other: Shape) -> Shape:
        if self.size != other.size:
            raise ValueError("Shapes need to have the same sizes.")
        self.mask ^= other.mask
        return self

    def __sub__(self, other: Shape) -> Shape:
        if self.size != other.size:
            raise ValueError("Shapes need to have the same sizes.")
        return Shape.from_array(self.mask & ~other.mask)

    def __isub__(self, other: Shape) -> Shape:
        if self.size != other.size:
            raise ValueError("Shapes need to have the same sizes.")
        self.mask &= ~other.mask
        return self

    def __invert__(self) -> Shape:
        return Shape.from_array(~self.mask)

    def intersection(
        self,
        origin_first: Vector,
        first: Shape,
        origin_second: Vector,
        second: Shape,
    ) -> Shape:
        """Returns an intersection of two shapes as if they have been placed according
        to the given origins."""
        if not origin_first.is_positive() or not origin_second.is_positive():
            raise ValueError("The origin of the shape has to be positive.")
        first_larger = Shape.empty(self.size)
        first_larger.insert_shape(origin_first, first)

        second_larger = Shape.empty(self.size)
        second_larger.insert_shape(origin_second, second)

        return first_larger & second_larger

    def volume(self) -> int:
        """Returns a number of true points."""
        return np.count_nonzero(self.mask)

    # TODO just make it __str__.
    def print(self) -> None:
        """Convenient print."""
        image = np.where(self._mask, "■", "□")
        print(image)

    def inside_bbox(self, p: Vector) -> bool:
        """Checks whether a point is inside the bounding box of the shape."""
        return 0 <= p.y < self.h and 0 <= p.x < self.w

    def is_inside_mask(self, p: Vector) -> bool:
        """Checks whether a point is inside the mask."""
        if not self.inside_bbox(p):
            return False
        return bool(self.mask[p.y, p.x])

    def is_subset_of(self, other: Shape) -> bool:
        """Checks whether the shape is subset of another."""
        if self.size != other.size:
            return False
        return np.all(other.mask & self.mask == self.mask)

    # TODO rename this
    def is_empty(self) -> bool:
        """Return true if there are no true elements"""
        return not np.any(self.mask)

    def insert_shape(self, origin: Vector, to_put: Shape) -> Shape:
        """Inserts another shape inside with respect to its origin and mask."""
        self._set_mask_values(origin, to_put, True)
        return self

    def remove_shape(self, origin: Vector, to_remove: Shape) -> Shape:
        """Removes another shape defined by its true values with respect to its
        origin."""
        self._set_mask_values(origin, to_remove, False)
        return self

    def border(self, thickness: int = 1, direction: Direction = None) -> Shape:
        """Returns a border of the given thickness in the given direction.
        Border in all direction will be returned if direction is None."""
        if thickness < 0:
            raise ValueError("Thickness cannot be negative.")
        if thickness == 0:
            return Shape.empty(self.size)
        if direction is None:
            return Shape.from_array(
                self.mask
                & ~binary_erosion(self.mask, structure=SQUARE, iterations=thickness)
            )
        structure = VERTICAL if direction.is_vertical() else HORIZONTAL
        if direction == direction.EAST:
            origin = (0, -1)
        elif direction == direction.SOUTH:
            origin = (-1, 0)
        else:
            origin = (0, 0)
        return Shape.from_array(
            self.mask & ~binary_erosion(self.mask, structure, origin=origin)
        )

    def corners(self) -> Shape:
        """Returns all the corners."""
        result = Shape.empty(self.size)
        for dir in Direction.get_all_directions():
            result |= self.corners_in_direction(dir)
        return result

    def corners_in_direction(self, direction: Direction) -> Shape:
        """Returns all the corners in a given direction. The given direction and
        its clockwise neighbour specifies the corner orientation."""
        corner = INSIDE_CORNERS.get(direction)
        return Shape.from_array(
            binary_hit_or_miss(self.mask, structure1=corner[0], origin1=corner[1])
        )

    def outside_corners_in_direction(self, direction: Direction) -> Shape:
        """Returns all the outside corners in a given direction. The given direction and
        its clockwise neighbour specifies the corner orientation."""
        corner = OUTSIDE_CORNERS.get(direction)
        return Shape.from_array(
            binary_hit_or_miss(self.mask, structure1=corner[0], origin1=corner[1])
        )

    def outside_corners(self) -> Shape:
        """Returns all the outside corners."""
        result = Shape.empty(self.size)
        for dir in Direction.get_all_directions():
            result |= self.outside_corners_in_direction(dir)
        return result

    def connected_border(self) -> Shape:
        """Returns a border without the shape's outside corners."""
        return self.border() - self.corners() - self.outside_corners()

    def points(self) -> list[Vector]:
        """Returns a list of all true valued points."""
        result = []
        for y, x in np.argwhere(self.mask):
            result.append(Vector(y, x))
        return result

    def sample(self) -> Vector:
        """Samples and returns a position of a true value within the shape."""
        if self.is_empty():
            raise ValueError("Cannot sample from an empty shape.")
        sample = random.choice(np.argwhere(self.mask))
        return Vector(sample[0], sample[1])

    def fit_in(
        self, to_fit: Shape, anchor: Shape = None, to_fit_anchor: Shape = None
    ) -> Shape:
        """Returns a shape of the same size with true values where the given
        shape fits inside. anchor defines the places of the object the shape to
        fit needs to touch. to_fit_anchor defines the places of to_fit which
        need to touch the object anchor. Both of these equals to their
        reciprocate objects if None."""
        if anchor is None:
            anchor = deepcopy(self)
        if to_fit_anchor is None:
            to_fit_anchor = deepcopy(to_fit)
        if self.size != anchor.size:
            raise ValueError("Anchor has to have the same size as the object.")
        if not anchor.is_subset_of(self):
            raise ValueError("Anchor has to be subset of the object.")
        if to_fit.size != to_fit_anchor.size:
            raise ValueError(
                "The object to fit has to have the same size as its anchor."
            )
        if not to_fit_anchor.is_subset_of(to_fit):
            raise ValueError("The object to fit has to be a superset of its anchor.")

        normalised_origin = (-(to_fit.h // 2), -(to_fit.w // 2))
        structure = to_fit.mask
        # For dilation the structure and its origin needs to be flipped.
        # Scipy library thing.
        flipped_origin = ((to_fit.h - 1) // 2, (to_fit.w - 1) // 2)
        flipped_structure = np.flip(to_fit_anchor.mask)
        fits_in = binary_erosion(
            self.mask, structure=structure, origin=normalised_origin
        )
        touches_anchor = binary_dilation(
            anchor.mask, structure=flipped_structure, origin=flipped_origin
        )
        return Shape.from_array(fits_in & touches_anchor)

        # TODO detect neighbours and create doors randomly
