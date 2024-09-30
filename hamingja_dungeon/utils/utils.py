import numpy as np
from scipy.ndimage import distance_transform_edt

from hamingja_dungeon.areas.morphology.morphology import prune


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
