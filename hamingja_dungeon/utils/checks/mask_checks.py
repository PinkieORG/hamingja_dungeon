from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hamingja_dungeon.dungeon_elements.mask import Mask
from hamingja_dungeon.utils.vector import Vector


def check_masks_are_same_size(first_mask: Mask, second_mask: Mask) -> None:
    if first_mask.size != second_mask.size:
        raise ValueError("Shapes need to have the same sizes.")


def check_vector_is_positive(vector: Vector) -> None:
    if not vector.is_positive():
        raise ValueError("The origin of the mask has to be positive.")


def check_thickness_is_positive(thickness: int) -> None:
    if thickness < 0:
        raise ValueError("Thickness cannot be negative.")