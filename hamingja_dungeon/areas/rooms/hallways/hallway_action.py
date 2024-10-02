from __future__ import annotations

from hamingja_dungeon.areas.vector import Vector
from hamingja_dungeon.direction.direction import Direction


class HallwayAction:
    """An action that can be performed during drawing of the hallway.
    Has a condition that specify if the subsequent effect can be performed."""

    def __init__(self, condition, effect):
        self.condition = condition
        self.effect = effect


def get_all_actions() -> dict[str, HallwayAction]:
    from hamingja_dungeon.areas.rooms.hallways.hallway_designer import HallwayDesigner

    def _valid_head(
        designer: HallwayDesigner, head: Vector, direction: Direction
    ) -> bool:
        """Checks if the new head of the drawing process is valid; i.e. it's inside
        the area, it doesn't collide with itself e.g."""
        neighbours = head.neighbours()
        for neighbour in neighbours:
            if not designer.dungeon_area.is_inside_area(neighbour):
                return False
        # TODO childless area without child borders in the future.
        if not designer.dungeon_area.in_childless_area(head):
            return False
        if head in designer.points:
            return False
        front = head + direction.unit_vector()
        front_left = front + direction.left().unit_vector()
        front_right = front + direction.right().unit_vector()
        front_neighbours = [front, front_left, front_right]
        for front_neighbour in front_neighbours:
            if front_neighbour in designer.points:
                return False
        return True

    def _move(
        designer: HallwayDesigner, head: Vector, direction: Direction = None
    ) -> None:
        """Set the designers parameters correctly after a moving action."""
        designer.points.append(head)
        designer.head_point = head
        if direction is not None:
            designer.direction = direction
        designer.length += 1

    result = {}

    def forward_condition(designer: HallwayDesigner) -> bool:
        new_head = designer.head_point + designer.direction.unit_vector()
        return _valid_head(designer, new_head, designer.direction)

    def forward_effect(designer: HallwayDesigner) -> None:
        new_head = designer.head_point + designer.direction.unit_vector()
        _move(designer, new_head)

    result["move_forward"] = HallwayAction(
        condition=forward_condition, effect=forward_effect
    )

    def right_condition(designer: HallwayDesigner) -> bool:
        new_direction = designer.direction.right()
        new_head = designer.head_point + new_direction.unit_vector()
        return _valid_head(designer, new_head, new_direction)

    def right_effect(designer: HallwayDesigner) -> None:
        new_direction = designer.direction.right()
        new_head = designer.head_point + new_direction.unit_vector()
        _move(designer, new_head, new_direction)

    result["turn_right"] = HallwayAction(condition=right_condition, effect=right_effect)

    def left_condition(designer: HallwayDesigner) -> bool:
        new_direction = designer.direction.left()
        new_head = designer.head_point + new_direction.unit_vector()
        return _valid_head(designer, new_head, new_direction)

    def left_effect(designer: HallwayDesigner) -> None:
        new_direction = designer.direction.left()
        new_head = designer.head_point + new_direction.unit_vector()
        _move(designer, new_head, new_direction)

    result["turn_left"] = HallwayAction(condition=left_condition, effect=left_effect)

    return result
