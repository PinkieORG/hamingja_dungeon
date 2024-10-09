from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
if TYPE_CHECKING:
    from hamingja_dungeon.dungeon_elements.area import AreaWithOrigin
from hamingja_dungeon.tile_types import tile_dt


def check_value_is_tile_type(value: np.ndarray) -> None:
    if value.dtype != tile_dt:
        raise ValueError("Fill value has to have the tile dtype.")


def check_child_of_id_exists(
    child_id: int, children: dict[int, AreaWithOrigin]
) -> None:
    if child_id not in children:
        raise ValueError("A child of this id does not exist.")
