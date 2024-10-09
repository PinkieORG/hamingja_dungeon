import numpy as np


def check_array_is_two_dimensional(array: np.ndarray) -> None:
    if array.ndim != 2:
        raise ValueError("The given array has to be 2 dimensional.")


def check_array_is_same_shape(
    first_array: np.ndarray, second_array: np.ndarray
) -> None:
    if first_array.shape != second_array.shape:
        raise ValueError("The given array has to have a same shape.")
