from enum import Enum
import numpy as np


FOUR_CONNECTIVITY = np.array([[-1, 0], [0, 1], [1, 0], [0, -1]])
EIGHT_CONNECTIVITY = np.concatenate(
    [np.array([[-1, -1], [1, -1], [-1, 1], [1, 1]]), FOUR_CONNECTIVITY]
)


class Connectivity(Enum):
    FOUR = 4
    EIGHT = 8

    def get_adjacency_mask(self):
        if self == Connectivity.FOUR:
            return FOUR_CONNECTIVITY
        if self == Connectivity.EIGHT:
            return EIGHT_CONNECTIVITY
        else:
            raise ValueError("Invalid connectivity.")
