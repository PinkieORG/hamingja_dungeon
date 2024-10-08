from copy import deepcopy

import numpy as np
from scipy.ndimage import binary_hit_or_miss

from hamingja_dungeon.utils.morphology.structure_elements.structure_elements import ENDPOINTS


def prune(array: np.array, iterations: int = 1) -> np.array:
    """Removes endpoints from an array."""
    if iterations < 0:
        raise ValueError("Iteration cannot be negative.")

    result = deepcopy(array)
    for _ in range(iterations):
        endpoints = get_endpoints(result)
        result ^= endpoints
    return result


def get_endpoints(array: np.array) -> np.array:
    """Returns all endpoints of an array"""
    result = np.zeros(array.shape).astype(bool)
    for structure in ENDPOINTS.values():
        result = result | binary_hit_or_miss(
            array,
            structure1=structure.fg,
            structure2=structure.bg,
            origin1=structure.origin,
        )
    return result
