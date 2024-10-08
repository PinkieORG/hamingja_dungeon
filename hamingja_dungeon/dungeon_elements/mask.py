from __future__ import annotations

import random
from copy import deepcopy
from typing import Tuple

import numpy as np
from scipy.ndimage import binary_erosion, binary_hit_or_miss, binary_dilation

from hamingja_dungeon.utils.checks.array_checks import check_array_is_two_dimensional, \
    check_array_is_same_shape
from hamingja_dungeon.utils.checks.mask_checks import check_vector_is_positive, \
    check_masks_are_same_size
from hamingja_dungeon.utils.direction import Direction
from hamingja_dungeon.utils.morphology.structure_elements import (OUTSIDE_CORNERS,
                                                                  SQUARE, HORIZONTAL,
                                                                  VERTICAL,
                                                                  INSIDE_CORNERS, )
from hamingja_dungeon.utils.vector import Vector


class Mask:
    """Represents a binary area."""

    def __init__(self, size: Tuple[int, int]):
        if size[0] <= 0 or size[1] <= 0:
            raise ValueError("The size has to be positive.")
        self._array = np.full(size, fill_value=True, dtype=np.bool)

    def _crop_array(self, origin: Vector, size: Tuple[int, int]) -> np.array:
        """Returns a cropped array from the given origin given by the size."""
        check_vector_is_positive(origin)
        return self.array[origin.y : origin.y + size[0], origin.x : origin.x + size[1]]

    def _set_array_values(self, origin: Vector, mask: Mask, set_to: bool) -> None:
        """Sets values defined by the true values of the new mask inserted to
        the given origin."""
        afflicted_area = self._crop_array(origin, mask.size)
        cropped_mask = mask._crop_array(Vector(0, 0), afflicted_area.shape)
        afflicted_area[cropped_mask] = set_to

    @staticmethod
    def from_array(in_array: np.ndarray) -> Mask:
        """Creates a new mask from a numpy array."""
        check_array_is_two_dimensional(in_array)
        result = Mask((in_array.shape[0], in_array.shape[1]))
        result.array = np.array(in_array, dtype=bool)
        return result

    @staticmethod
    def empty_mask(size: Tuple[int, int]) -> Mask:
        """Creates an empty mask of the given size."""
        shape = Mask(size)
        shape.array.fill(False)
        return shape

    @property
    def size(self) -> Tuple[int, int]:
        return self.h, self.w

    @property
    def h(self) -> int:
        return self.array.shape[0]

    @property
    def w(self) -> int:
        return self.array.shape[1]

    @property
    def array(self) -> np.ndarray:
        return self._array

    @array.setter
    def array(self, new_array: np.ndarray) -> None:
        check_array_is_two_dimensional(new_array)
        check_array_is_same_shape(self.array, new_array)
        self._array = new_array

    def __str__(self) -> str:
        return str(np.where(self._array, "■", "□"))

    def __and__(self, other: Mask) -> Mask:
        check_masks_are_same_size(self, other)
        return Mask.from_array(self.array & other.array)

    def __iand__(self, other: Mask) -> Mask:
        check_masks_are_same_size(self, other)
        self.array &= other.array
        return self

    def __or__(self, other: Mask) -> Mask:
        check_masks_are_same_size(self, other)
        return Mask.from_array(self.array | other.array)

    def __ior__(self, other: Mask) -> Mask:
        check_masks_are_same_size(self, other)
        self.array |= other.array
        return self

    def __xor__(self, other: Mask) -> Mask:
        check_masks_are_same_size(self, other)
        return Mask.from_array(self.array ^ other.array)

    def __ixor__(self, other: Mask) -> Mask:
        check_masks_are_same_size(self, other)
        self.array ^= other.array
        return self

    def __sub__(self, other: Mask) -> Mask:
        check_masks_are_same_size(self, other)
        return Mask.from_array(self.array & ~other.array)

    def __isub__(self, other: Mask) -> Mask:
        check_masks_are_same_size(self, other)
        self.array &= ~other.array
        return self

    def __invert__(self) -> Mask:
        return Mask.from_array(~self.array)

    def intersection(
        self,
        first_origin: Vector,
        first_mask: Mask,
        second_origin: Vector,
        second_mask: Mask,
    ) -> Mask:
        """Returns an intersection of two shapes as if they have been placed according
        to the given origins."""
        first_embedded = Mask.empty_mask(self.size)
        first_embedded.insert_shape(first_origin, first_mask)
        second_embedded = Mask.empty_mask(self.size)
        second_embedded.insert_shape(second_origin, second_mask)
        return first_embedded & second_embedded

    def volume(self) -> int:
        """Returns a number of true points."""
        return np.count_nonzero(self.array)

    def inside_bbox(self, p: Vector) -> bool:
        """Checks whether a point is inside the bounding box of the shape."""
        return 0 <= p.y < self.h and 0 <= p.x < self.w

    def is_inside_mask(self, p: Vector) -> bool:
        """Checks whether a point is inside the mask."""
        if not self.inside_bbox(p):
            return False
        return bool(self.array[p.y, p.x])

    def is_subset_of(self, other: Mask) -> bool:
        """Checks whether the shape is subset of another."""
        if self.size != other.size:
            return False
        return np.all(other.array & self.array == self.array)

    # TODO rename this
    def is_empty(self) -> bool:
        """Return true if there are no true elements"""
        return not np.any(self.array)

    def insert_shape(self, origin: Vector, to_insert: Mask) -> Mask:
        """Inserts another shape inside with respect to its origin and mask."""
        self._set_array_values(origin, to_insert, True)
        return self

    def remove_shape(self, origin: Vector, to_remove: Mask) -> Mask:
        """Removes another shape defined by its true values with respect to its
        origin."""
        self._set_array_values(origin, to_remove, False)
        return self

    def border(self, thickness: int = 1, direction: Direction = None) -> Mask:
        """Returns a border of the given thickness in the given direction.
        Border in all direction will be returned if direction is None."""
        if thickness < 0:
            raise ValueError("Thickness cannot be negative.")
        if thickness == 0:
            return Mask.empty_mask(self.size)
        if direction is None:
            return Mask.from_array(
                self.array
                & ~binary_erosion(self.array, structure=SQUARE, iterations=thickness)
            )
        structure = VERTICAL if direction.is_vertical() else HORIZONTAL
        if direction == direction.EAST:
            origin = (0, -1)
        elif direction == direction.SOUTH:
            origin = (-1, 0)
        else:
            origin = (0, 0)
        return Mask.from_array(
            self.array & ~binary_erosion(self.array, structure, origin=origin)
        )

    def corners(self) -> Mask:
        """Returns all the corners."""
        result = Mask.empty_mask(self.size)
        for dir in Direction.get_all_directions():
            result |= self.corners_in_direction(dir)
        return result

    def corners_in_direction(self, direction: Direction) -> Mask:
        """Returns all the corners in a given direction. The given direction and
        its clockwise neighbour specifies the corner orientation."""
        corner = INSIDE_CORNERS.get(direction)
        return Mask.from_array(
            binary_hit_or_miss(self.array, structure1=corner[0], origin1=corner[1])
        )

    def outside_corners_in_direction(self, direction: Direction) -> Mask:
        """Returns all the outside corners in a given direction. The given direction and
        its clockwise neighbour specifies the corner orientation."""
        corner = OUTSIDE_CORNERS.get(direction)
        return Mask.from_array(
            binary_hit_or_miss(self.array, structure1=corner[0], origin1=corner[1])
        )

    def outside_corners(self) -> Mask:
        """Returns all the outside corners."""
        result = Mask.empty_mask(self.size)
        for dir in Direction.get_all_directions():
            result |= self.outside_corners_in_direction(dir)
        return result

    def connected_border(self) -> Mask:
        """Returns a border without the shape's outside corners."""
        return self.border() - self.corners() - self.outside_corners()

    def points(self) -> list[Vector]:
        """Returns a list of all true valued points."""
        result = []
        for y, x in np.argwhere(self.array):
            result.append(Vector(y, x))
        return result

    def sample(self) -> Vector:
        """Samples and returns a position of a true value within the shape."""
        if self.is_empty():
            raise ValueError("Cannot sample from an empty shape.")
        sample = random.choice(np.argwhere(self.array))
        return Vector(sample[0], sample[1])

    def fit_in(
        self, to_fit: Mask, anchor: Mask = None, to_fit_anchor: Mask = None
    ) -> Mask:
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
        structure = to_fit.array
        # For dilation the structure and its origin needs to be flipped.
        # Scipy library thing.
        flipped_origin = ((to_fit.h - 1) // 2, (to_fit.w - 1) // 2)
        flipped_structure = np.flip(to_fit_anchor.array)
        fits_in = binary_erosion(
            self.array, structure=structure, origin=normalised_origin
        )
        touches_anchor = binary_dilation(
            anchor.array, structure=flipped_structure, origin=flipped_origin
        )
        return Mask.from_array(fits_in & touches_anchor)

        # TODO detect neighbours and create doors randomly
