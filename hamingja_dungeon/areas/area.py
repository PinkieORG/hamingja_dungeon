from __future__ import annotations

import random
from copy import deepcopy
from typing import Tuple

import numpy as np
from scipy.ndimage import binary_erosion, binary_hit_or_miss, binary_dilation

from hamingja_dungeon.areas.morphology.structure_elements import (
    SQUARE,
    HORIZONTAL,
    VERTICAL,
    CORNERS,
)
from hamingja_dungeon.areas.vector import Vector
from hamingja_dungeon.direction.direction import Direction


class Area:
    """Represents a binary area."""

    def __init__(self, size: Tuple[int, int]):
        if size[0] <= 0 or size[1] <= 0:
            raise ValueError("The size has to be positive.")
        self._mask = np.full(size, fill_value=True, dtype=np.bool)

    def _set_mask_values(self, origin: Vector, mask: Area, set_to: bool) -> None:
        """Sets values defined by the true values of the new mask inserted to
        the given origin."""
        if not origin.is_positive():
            raise ValueError("The origin of the area has to be positive.")
        afflicted_area = self.mask[
            origin.y : origin.y + mask.h, origin.x : origin.x + mask.w
        ]
        if 0 in afflicted_area.shape:
            return
        cropped_mask = mask.mask[
            0 : afflicted_area.shape[0], 0 : afflicted_area.shape[1]
        ]
        afflicted_area[cropped_mask] = set_to

    @staticmethod
    def from_array(in_array: np.ndarray) -> Area:
        """Creates a new area from a numpy array."""
        mask = np.array(in_array, dtype=bool)
        if mask.ndim != 2:
            raise ValueError("The given array has to be 2 dimensional.")
        result = Area((mask.shape[0], mask.shape[1]))
        result.mask = mask
        return result

    @staticmethod
    def empty_area(size: Tuple[int, int]) -> Area:
        area = Area(size)
        area.mask.fill(False)
        return area

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

    def __and__(self, other: Area) -> Area:
        if self.size != other.size:
            raise ValueError("Areas need to have the same sizes.")
        return Area.from_array(self.mask & other.mask)

    def __iand__(self, other: Area) -> Area:
        if self.size != other.size:
            raise ValueError("Areas need to have the same sizes.")
        self.mask &= other.mask
        return self

    def __or__(self, other: Area) -> Area:
        if self.size != other.size:
            raise ValueError("Areas need to have the same sizes.")
        return Area.from_array(self.mask | other.mask)

    def __ior__(self, other: Area) -> Area:
        if self.size != other.size:
            raise ValueError("Areas need to have the same sizes.")
        self.mask |= other.mask
        return self

    def __xor__(self, other: Area) -> Area:
        if self.size != other.size:
            raise ValueError("Areas need to have the same sizes.")
        return Area.from_array(self.mask ^ other.mask)

    def __ixor__(self, other: Area) -> Area:
        if self.size != other.size:
            raise ValueError("Areas need to have the same sizes.")
        self.mask ^= other.mask
        return self

    def __sub__(self, other: Area) -> Area:
        if self.size != other.size:
            raise ValueError("Areas need to have the same sizes.")
        return Area.from_array(self.mask & ~other.mask)

    def __isub__(self, other: Area) -> Area:
        if self.size != other.size:
            raise ValueError("Areas need to have the same sizes.")
        self.mask &= ~other.mask
        return self

    def __invert__(self) -> Area:
        return Area.from_array(~self.mask)

    def intersection(
        self,
        origin_first: Vector,
        first: Area,
        origin_second: Vector,
        second: Area,
    ) -> Area:
        """Returns an intersection of two areas."""
        if not origin_first.is_positive() or not origin_second.is_positive():
            raise ValueError("The origin of the area has to be positive.")
        first_larger = Area.empty_area(self.size)
        first_larger.insert_area(origin_first, first)

        second_larger = Area.empty_area(self.size)
        second_larger.insert_area(origin_second, second)

        return first_larger & second_larger

    def volume(self) -> int:
        """Returns a number of true points."""
        return np.count_nonzero(self.mask)

    def print(self) -> None:
        """Convenient print."""
        image = np.where(self._mask, "■", "□")
        print(image)

    def inside_bbox(self, p: Vector) -> bool:
        """Checks whether a point is inside the bounding box of the area."""
        return 0 <= p.y < self.h and 0 <= p.x < self.w

    def is_inside_area(self, p: Vector) -> bool:
        """Checks whether a point is inside the area."""
        if not self.inside_bbox(p):
            return False
        return bool(self.mask[p.y, p.x])

    def is_subset_of(self, other: Area) -> bool:
        """Checks whether the area is subset of another."""
        if self.size != other.size:
            return False
        return np.all(other.mask & self.mask == self.mask)

    # TODO rename this
    def is_empty(self):
        """Return true if there are no true elements"""
        return not np.any(self.mask)

    def insert_area(self, origin: Vector, to_put: Area) -> Area:
        """Inserts another area inside with respect to its origin and mask."""
        self._set_mask_values(origin, to_put, True)
        return self

    def remove_area(self, origin: Vector, to_remove: Area) -> Area:
        """Removes another area defined by its true values with respect to its
        origin."""
        self._set_mask_values(origin, to_remove, False)
        return self

    def border(self, thickness: int = 1) -> Area:
        """Returns a border of the given thickness."""
        if thickness < 0:
            raise ValueError("Thickness cannot be negative.")
        if thickness == 0:
            return Area.empty_area(self.size)
        return Area.from_array(
            self.mask
            & ~binary_erosion(self.mask, structure=SQUARE, iterations=thickness)
        )

    def border_in_direction(self, direction: Direction) -> Area:
        """Returns a border in the specific direction."""
        structure = VERTICAL if direction.is_vertical() else HORIZONTAL
        if direction == direction.EAST:
            origin = (0, -1)
        elif direction == direction.SOUTH:
            origin = (-1, 0)
        else:
            origin = (0, 0)
        return Area.from_array(
            self.mask & ~binary_erosion(self.mask, structure, origin=origin)
        )

    def corners(self) -> Area:
        """Returns all the corners."""
        result = Area.empty_area(self.size)
        for dir in Direction.get_all_directions():
            result |= self.corners_in_direction(dir)
        return result

    def corners_in_direction(self, direction: Direction) -> Area:
        """Returns all the corners in a given direction. The given direction and
        its clockwise neighbour specifies the corner orientation."""
        corner = CORNERS.get(direction)
        return Area.from_array(
            binary_hit_or_miss(self.mask, structure1=corner[0], origin1=corner[1])
        )

    def connected_border(self) -> Area:
        """Returns a border without the area's outside corners."""
        return self.border() - self.corners()

    def sample(self) -> Vector:
        """Samples and returns a position of a true value within the area."""
        if self.is_empty():
            raise ValueError("Cannot sample from an empty area.")
        sample = random.choice(np.argwhere(self.mask))
        return Vector(sample[0], sample[1])

    def fit_in(
        self, to_fit: Area, anchor: Area = None, to_fit_anchor: Area = None
    ) -> Area:
        """Returns an area of the same size with true values where the given
        area fits inside. anchor defines the places of the object the area to
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
        return Area.from_array(fits_in & touches_anchor)

        # TODO detect neighbours and create doors randomly
