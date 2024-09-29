from enum import Enum


class Orientation(Enum):
    VERTICAL = 0
    HORIZONTAL = 1

    def get_axis(self):
        return (self.value + 1) % 2
