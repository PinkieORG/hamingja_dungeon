from __future__ import annotations

import random
from typing import Tuple


class DimensionSampler:
    """
    Can be sampled randomly according to minimum and maximum dimensions.
    """

    def __init__(self, dim_range: Tuple[int, int, int, int]):
        min_h, max_h, min_w, max_w = dim_range
        if min_h > max_h or min_w > max_w:
            raise ValueError(
                "Minimum dimension cannot be larger than the maximum "
                "dimension."
                f"Got min_h: {min_h}, max_h: {max_h}, "
                f"min_w: {min_w}, max_w: {max_w}",
            )
        if min_h == 0 or min_w == 0:
            raise ValueError(
                "Minimum dimension cannot be zero. ",
                f"Got min_h: {min_h}, max_h: {max_h}, "
                f"min_w: {min_w}, max_w: {max_w}",
            )
        self.min_h = min_h
        self.max_h = max_h
        self.min_w = min_w
        self.max_w = max_w

    @staticmethod
    def as_factor(
        size: Tuple, size_factors: Tuple[float, float, float, float]
    ) -> DimensionSampler:
        """
        Creates a new DimensionRange. Its min/max height will be calculated by
        multiplying the first two numbers in size_factors by the given height.
        Same for width with second two numbers in size_factors. The resulting
        minimum dimensions are rounded to 1 if less than 1.
        """
        for dim in size_factors:
            if dim <= 0 or dim > 1:
                raise ValueError(
                    f"Factors have to be between zero and one. " f"Got {dim}."
                )
        min_h = int(size[0] * size_factors[0])
        if min_h <= 1:
            min_h = 1
        max_h = int(size[0] * size_factors[1])
        if min_h >= max_h:
            max_h = min_h + 1
        min_w = int(size[1] * size_factors[2])
        if min_w <= 1:
            min_w = 1
        max_w = int(size[1] * size_factors[3])
        if min_w >= max_w:
            max_w = min_w + 1
        return DimensionSampler((min_h, max_h, min_w, max_w))

    @staticmethod
    def fixed(dimension: Tuple[int, int]):
        return DimensionSampler(
            (dimension[0], dimension[0], dimension[1], dimension[1])
        )

    def sample(self) -> Tuple[int, int]:
        if self.min_h == self.max_h:
            h = self.min_h
        else:
            h = random.randrange(self.min_h, self.max_h)

        if self.min_w == self.max_w:
            w = self.min_w
        else:
            w = random.randrange(self.min_w, self.max_w)

        return h, w
