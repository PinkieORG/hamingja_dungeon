from __future__ import annotations


import random
from dataclasses import dataclass
from typing import List, Tuple

import numpy as np

from hamingja_dungeon.areas.dungeon_area import DungeonArea
from hamingja_dungeon.areas.rooms.hallways.hallway_action import (
    HallwayAction,
    get_all_actions,
)
from hamingja_dungeon.areas.rooms.hallways.hallway_action_manager import (
    CannotPerformAction,
)
from hamingja_dungeon.areas.vector import Vector
from hamingja_dungeon.areas.rooms.hallways.hallway import Hallway
from hamingja_dungeon.direction.direction import Direction


class HallwayDesigner:
    @dataclass
    class Action:
        object: HallwayAction
        base_likelihood: float
        base_cooldown: int
        likelihood: float
        cooldown: int

        def on_cooldown(self) -> bool:
            return self.cooldown < self.base_cooldown

        def tick_cooldown(self) -> None:
            if self.cooldown < self.base_cooldown:
                self.cooldown += 1

        def reset_cooldown(self) -> None:
            self.cooldown = 0

    def __init__(self, dungeon_area: DungeonArea):

        # to config in the future
        self.max_length = 20

        self.length = 0
        self.head_point = None
        self.points = []
        self.direction = None

        self.dungeon_area = dungeon_area
        all_actions = get_all_actions()
        # hardcoded
        self.actions = {
            "move_forward": self.Action(
                object=all_actions.get("move_forward"),
                base_likelihood=0.6,
                base_cooldown=0,
                likelihood=0.6,
                cooldown=0,
            ),
            "turn_left": self.Action(
                object=all_actions.get("turn_left"),
                base_likelihood=0.2,
                base_cooldown=2,
                likelihood=0.2,
                cooldown=2,
            ),
            "turn_right": self.Action(
                object=all_actions.get("turn_right"),
                base_likelihood=0.2,
                base_cooldown=2,
                likelihood=0.2,
                cooldown=2,
            ),
        }

    def _get_possible_actions(self) -> list[Action]:
        result = []
        for name, action in self.actions.items():
            if action.on_cooldown():
                continue
            if action.object.condition(self):
                result.append(action)
        return result

    def _choose_action(self) -> Action:
        possible_actions = self._get_possible_actions()
        weights = [action.likelihood for action in possible_actions]
        return random.choices(possible_actions, weights=weights)[0]

    def _perform_action(self, action: Action) -> None:
        action.object.effect(self)
        for a in self.actions.values():
            a.tick_cooldown()
        action.reset_cooldown()

    def _step(self):
        try:
            action = self._choose_action()
        except IndexError:
            raise CannotPerformAction
        self._perform_action(action)

    def _create_hallway(self):
        ys = list(map(lambda p: p.y, self.points))
        xs = list(map(lambda p: p.x, self.points))

        min_y = min(ys)
        min_x = min(xs)
        origin = Vector(min_y, min_x)
        max_y = max(ys)
        max_x = max(xs)
        size = (max_y - min_y + 1, max_x - min_x + 1)

        path = np.zeros(size).astype(bool)

        hallway_points = [p - origin for p in self.points]

        for point in hallway_points:
            path[point.y, point.x] = True

        hallway = Hallway(path)
        origin.y -= 1
        origin.x -= 1
        return origin, hallway

    def _setup(
        self,
        start_point: Vector,
        possible_direction: List[Direction],
    ):
        self.points.append(start_point)
        self.direction = random.choice(possible_direction)
        self.length = 1
        self.head_point = start_point

    def design_hallway(
        self,
        start_point: Vector,
        possible_direction: List[Direction],
    ) -> Tuple[Vector, Hallway]:
        self._setup(start_point, possible_direction)
        while self.length <= self.max_length:
            try:
                self._step()
            except CannotPerformAction:
                break
        return self._create_hallway()
