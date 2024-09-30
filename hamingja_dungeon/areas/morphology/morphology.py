from copy import deepcopy

from scipy.ndimage import binary_hit_or_miss

from hamingja_dungeon.areas.area import Area
from hamingja_dungeon.areas.morphology.structure_elements import ENDPOINTS_4


def prune(area: Area, iterations: int = 1) -> Area:
    if iterations < 0:
        raise ValueError("Iteration cannot be negative.")

    result = deepcopy(area)
    for _ in range(iterations):
        endpoints = Area.empty_area(area.size)
        for structure in ENDPOINTS_4.values():
            endpoints.mask |= binary_hit_or_miss(
                result.mask,
                structure1=structure.hit,
                structure2=structure.miss,
                origin1=structure.origin,
            )
        result ^= endpoints
    return result
