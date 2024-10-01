from __future__ import annotations


import random
from typing import List, Tuple

import numpy as np

from hamingja_dungeon.areas.dungeon_area import DungeonArea
from hamingja_dungeon.areas.rooms.hallways.actions import get_all_actions
from hamingja_dungeon.areas.vector import Vector
from hamingja_dungeon.areas.rooms.hallways.hallway import Hallway
from hamingja_dungeon.direction.direction import Direction
from hamingja_dungeon.tile_types import carpet


class CannotMakeStep(Exception):
    pass


class HallwayDesigner:
    def __init__(self):
        # in config in the future
        self.max_length = 5
        self.possible_actions = ["move_forward", "turn_left", "turn_right"]

        self.length = 0
        self.head_point = None
        self.points = []
        self.direction = None
        self.area = None

    def _get_possible_actions(self):
        result = []
        for name, action in get_all_actions().items():
            if name in self.possible_actions and action.condition(self):
                result.append(action)
        return result

    def _make_step(self):
        possible_actions = self._get_possible_actions()
        if len(possible_actions) == 0:
            raise CannotMakeStep
        action = random.choice(possible_actions)
        action.effect(self)

    def _create_hallway(self):
        ys = list(map(lambda p: p.y, self.points))
        xs = list(map(lambda p: p.x, self.points))

        min_y = min(ys)
        min_x = min(xs)
        origin = Vector(min_y, min_x)
        max_y = max(ys)
        max_x = max(xs)
        size = (max_y - min_y + 1, max_x - min_x + 1)

        array = np.zeros((max_y - min_y + 1, max_x - min_x + 1)).astype(bool)

        hallway_points = [p - origin for p in self.points]

        for point in hallway_points:
            array[point.y, point.x] = True

        hallway = Hallway(size, border_thickness=0, fill_value=carpet)
        hallway.mask = array
        return origin, hallway

    def _setup(
        self,
        dungeon_area: DungeonArea,
        start_point: Vector,
        possible_direction: List[Direction],
    ):
        self.area = dungeon_area
        self.points.append(start_point)
        self.direction = random.choice(possible_direction)
        self.head_point = start_point + self.direction.unit_vector()
        self.points.append(self.head_point)
        self.length = 2

    def design_hallway(
        self,
        dungeon_area: DungeonArea,
        start_point: Vector,
        possible_direction: List[Direction],
    ) -> Tuple[Vector, Hallway]:
        self._setup(dungeon_area, start_point, possible_direction)
        while self.length <= self.max_length:
            try:
                self._make_step()
            except CannotMakeStep:
                break
        return self._create_hallway()
