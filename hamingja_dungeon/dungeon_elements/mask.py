from __future__ import annotations

import random
from typing import Tuple

import numpy as np
from scipy.ndimage import binary_erosion, binary_hit_or_miss, binary_dilation

from hamingja_dungeon.utils.checks.array_checks import (check_array_is_two_dimensional,
                                                        check_array_is_same_shape, )
from hamingja_dungeon.utils.checks.mask_checks import (check_vector_is_positive,
                                                       check_masks_are_same_size,
                                                       check_thickness_is_positive,
                                                       check_anchor_is_subset,
                                                       check_mask_is_not_empty, )
from hamingja_dungeon.utils.direction import Direction
from hamingja_dungeon.utils.morphology.structure_elements.structure_elements import (
    OUTSIDE_CORNERS, SQUARE, INSIDE_CORNERS, BORDERS_FOR_EROSION, )
from hamingja_dungeon.utils.morphology.structure_elements.utils import (
    center_to_top_left, center_to_bottom_right, )
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
    def from_array(array: np.ndarray) -> Mask:
        """Creates a new mask from a numpy array."""
        check_array_is_two_dimensional(array)
        result = Mask((array.shape[0], array.shape[1]))
        result.array = np.array(array, dtype=bool)
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
        """Returns an intersection of two masks as if they have been placed according
        to the given origins."""
        first_embedded = Mask.empty_mask(self.size)
        first_embedded.insert_shape(first_origin, first_mask)
        second_embedded = Mask.empty_mask(self.size)
        second_embedded.insert_shape(second_origin, second_mask)
        return first_embedded & second_embedded

    def volume(self) -> int:
        """Returns a number of true elements."""
        return np.count_nonzero(self.array)

    def is_inside_bbox(self, vector: Vector) -> bool:
        """Checks whether a coordinate is inside the bounding box of the mask."""
        return 0 <= vector.y < self.h and 0 <= vector.x < self.w

    def is_inside_mask(self, vector: Vector) -> bool:
        """Checks whether a coordinate is inside the mask."""
        if not self.is_inside_bbox(vector):
            return False
        return bool(self.array[vector.y, vector.x])

    def is_subset_of(self, other: Mask) -> bool:
        """Checks whether the mask is subset of another."""
        if self.size != other.size:
            return False
        return np.all(other.array & self.array == self.array)

    def is_empty(self) -> bool:
        """Return true if there are no true elements"""
        return not np.any(self.array)

    def insert_shape(self, origin: Vector, to_insert: Mask) -> Mask:
        """Inserts another mask inside with respect to its origin."""
        self._set_array_values(origin, to_insert, True)
        return self

    def remove_shape(self, origin: Vector, to_remove: Mask) -> Mask:
        """Removes another mask defined by its true values with respect to its
        origin."""
        self._set_array_values(origin, to_remove, False)
        return self

    def border_in_direction(self, direction: Direction, thickness: int = 1) -> Mask:
        """Returns border in the given direction."""
        check_thickness_is_positive(thickness)
        structure = BORDERS_FOR_EROSION.get(direction)
        return Mask.from_array(
            self.array
            & ~binary_erosion(
                self.array,
                structure=structure.fg,
                origin=structure.origin,
                iterations=thickness,
            )
        )

    def border(self, thickness: int = 1) -> Mask:
        """Returns a border of the given thickness"""
        check_thickness_is_positive(thickness)
        return Mask.from_array(
            self.array
            & ~binary_erosion(
                self.array,
                structure=SQUARE.fg,
                origin=SQUARE.origin,
                iterations=thickness,
            )
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
            binary_hit_or_miss(self.array, structure1=corner.fg, origin1=corner.origin)
        )

    def outside_corners_in_direction(self, direction: Direction) -> Mask:
        """Returns all the outside corners in a given direction. The given direction and
        its clockwise neighbour specifies the corner orientation."""
        corner = OUTSIDE_CORNERS.get(direction)
        return Mask.from_array(
            binary_hit_or_miss(self.array, structure1=corner.fg, origin1=corner.origin)
        )

    def outside_corners(self) -> Mask:
        """Returns all the outside corners."""
        result = Mask.empty_mask(self.size)
        for dir in Direction.get_all_directions():
            result |= self.outside_corners_in_direction(dir)
        return result

    def border_without_corners(self) -> Mask:
        """Returns a border without the shape's outside corners."""
        return self.border() - self.corners() - self.outside_corners()

    def mask_coordinates(self) -> list[Vector]:
        """Returns a list of all coordinates that of the mask."""
        result = []
        for y, x in np.argwhere(self.array):
            result.append(Vector(y, x))
        return result

    def sample_mask_coordinate(self) -> Vector:
        """Samples and returns a coordinate of a true value within the mask."""
        check_mask_is_not_empty(self)
        sample = random.choice(np.argwhere(self.array))
        return Vector(sample[0], sample[1])

    def fit_in(self, to_fit: Mask) -> Mask:
        """Returns a mask that with the same size that defines at which coordinates
        the given mask fits entirely."""
        return Mask.from_array(
            binary_erosion(
                self.array,
                structure=to_fit.array,
                origin=center_to_top_left(to_fit.size),
            )
        )

    def fit_in_touching_anchor(self, to_fit: Mask, anchor: Mask):
        """Same as fit_in but the mask needs to additionally touch the coordinates
        given by an anchor."""
        check_masks_are_same_size(self, anchor)
        check_anchor_is_subset(self, anchor)
        touches_anchor = binary_dilation(
            anchor.array,
            structure=np.flip(to_fit.array),
            origin=center_to_bottom_right(to_fit.size),
        )
        return self.fit_in(to_fit) & Mask.from_array(touches_anchor)

    def fit_in_anchors_touching(self, to_fit: Mask, anchor: Mask, to_fit_anchor: Mask):
        """Same as fit_in_touching_anchor but the given the mask to fit comes with
        its own anchor that needs to touch this mask's anchor."""
        check_masks_are_same_size(self, anchor)
        check_anchor_is_subset(self, anchor)
        check_masks_are_same_size(to_fit, to_fit_anchor)
        check_anchor_is_subset(to_fit, to_fit_anchor)
        anchors_touching = binary_dilation(
            anchor.array,
            structure=np.flip(to_fit_anchor.array),
            origin=center_to_bottom_right(to_fit_anchor.size),
        )
        return self.fit_in(to_fit) & Mask.from_array(anchors_touching)
