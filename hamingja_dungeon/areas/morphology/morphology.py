from copy import deepcopy

import numpy as np
from scipy.ndimage import binary_hit_or_miss

from hamingja_dungeon.areas.morphology.structure_elements import ENDPOINTS_4


def prune(array: np.array, iterations: int = 1) -> np.array:
    if iterations < 0:
        raise ValueError("Iteration cannot be negative.")

    result = deepcopy(array)
    for _ in range(iterations):
        endpoints = np.zeros(array.shape).astype(bool)
        for structure in ENDPOINTS_4.values():
            endpoints = endpoints | binary_hit_or_miss(
                result,
                structure1=structure.hit,
                structure2=structure.miss,
                origin1=structure.origin,
            )
        result ^= endpoints
    return result
