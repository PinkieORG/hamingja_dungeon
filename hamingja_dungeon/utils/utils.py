import numpy as np
from scipy.ndimage import distance_transform_edt

from hamingja_dungeon.utils.morphology.morphology import prune


def tighten(array: np.array):
    """Shrinks the bounding box (np.array) so its tight around the True values."""
    non_zero_rows = np.where(np.any(array != 0, axis=1))[0]
    non_zero_columns = np.where(np.any(array != 0, axis=0))[0]

    return array[
        non_zero_rows.min() : non_zero_rows.max() + 1,
        non_zero_columns.min() : non_zero_columns.max() + 1,
    ]


def circle_mask(dim: int) -> np.array:
    """Returns a circle binary mask without the apexes on each side that do not
    border with the inside of the circle."""
    circle_dim = dim + 2
    without_middle = np.ones((circle_dim, circle_dim))
    without_middle[circle_dim // 2, circle_dim // 2] = 0
    distance_map = distance_transform_edt(without_middle)
    circle = distance_map <= circle_dim // 2
    circle = prune(circle)
    return circle[1:-1, 1:-1]
