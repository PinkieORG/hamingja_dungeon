from __future__ import annotations
import random
from dataclasses import dataclass
from typing import List, Tuple
import numpy as np
from hamingja_dungeon.dungeon_elements.sector import Sector
from hamingja_dungeon.hallway_designers.hallway_action import (
    HallwayAction,
    get_all_actions,
)
from hamingja_dungeon.utils.vector import Vector
from hamingja_dungeon.dungeon_elements.hallway import Hallway
from hamingja_dungeon.utils.direction import Direction


class CannotPerformAction(Exception):
    pass


class DesignerError(Exception):
    pass


class HallwayDesigner:
    """Creates hallways in the dungeon area. Draws a hallway path tile by tile
    according to customizable actions."""

    @dataclass
    class Action:
        """Utility class for storing action with their parameters."""

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

    def __init__(self, dungeon_area: Sector):
        self.dungeon_area = dungeon_area

        all_actions = get_all_actions()
        self._reset()

        # hardcoded to config in the future
        self.max_length = 30
        self.actions = {
            "move_forward": self.Action(
                object=all_actions.get("move_forward"),
                base_likelihood=0.6,
                base_cooldown=0,
                likelihood=3,
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

    def valid_head(self, head: Vector, direction: Direction) -> bool:
        """Checks if the new head of the drawing process is valid; i.e. it's inside
        the area, it doesn't collide with itself e.g."""
        neighbours = head.neighbours()
        for neighbour in neighbours:
            if not self.dungeon_area.is_inside_mask(neighbour):
                return False
        # TODO childless area without child borders in the future.
        if not self.dungeon_area.in_childless_area(head):
            return False
        if head in self.points:
            return False
        front = head + direction.unit_vector()
        front_left = front + direction.left().unit_vector()
        front_right = front + direction.right().unit_vector()
        front_neighbours = [front, front_left, front_right]
        for front_neighbour in front_neighbours:
            if front_neighbour in self.points:
                return False
        return True

    def _get_possible_actions(self) -> list[Action]:
        """Get a list of actions that are not on cooldown and their condition are
        met."""
        result = []
        for name, action in self.actions.items():
            if action.on_cooldown():
                continue
            if action.object.condition(self):
                result.append(action)
        return result

    def _choose_action(self) -> Action:
        """Randomly choose action with respect to its likelihood."""
        possible_actions = self._get_possible_actions()
        weights = [action.likelihood for action in possible_actions]
        return random.choices(possible_actions, weights=weights)[0]

    def _perform_action(self, action: Action) -> None:
        """Perform the given action."""
        action.object.effect(self)
        for a in self.actions.values():
            a.tick_cooldown()
        action.reset_cooldown()

    def _step(self) -> None:
        """Makes on step of the drawing process."""
        try:
            action = self._choose_action()
        except IndexError:
            raise CannotPerformAction
        self._perform_action(action)

    def _create_hallway(self) -> Tuple[Vector, Hallway]:
        """Creates a new hallway from the list of drawn hallway points and returns it
        along with its new origin on the dungeon area."""
        ys = list(map(lambda p: p.y, self.points))
        xs = list(map(lambda p: p.x, self.points))
        min_y, min_x, max_y, max_x = min(ys), min(xs), max(ys), max(xs)
        origin = Vector(min_y, min_x)
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
    ) -> None:
        """Initializes all the parameters used during the drawing and hallway creation
        stage."""
        directions = []
        for direction in possible_direction:
            head_point = start_point + direction.unit_vector()
            if self.valid_head(head_point, direction):
                directions.append(direction)
        if len(directions) == 0:
            raise DesignerError()
        initial_direction = random.choice(directions)
        self.head_point = start_point + initial_direction.unit_vector()
        self.points.append(self.head_point)
        self.direction = initial_direction
        self.length = 3

    def _reset(self) -> None:
        """Resets all the parameters used during the drawing and hallway creation
        stage."""
        self.length = 0
        self.head_point = None
        self.points = []
        self.direction = None

    def design_hallway(
        self,
        start_point: Vector,
        possible_direction: List[Direction],
    ) -> Tuple[Vector, Hallway]:
        """Returns a new hallway from the given starting point in the given initial
        direction along with its new origin."""
        self._setup(start_point, possible_direction)
        while self.length <= self.max_length:
            try:
                self._step()
            except CannotPerformAction:
                break
        origin, hallway = self._create_hallway()
        print(self.length)
        self._reset()
        return origin, hallway
