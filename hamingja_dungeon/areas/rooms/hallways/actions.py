from __future__ import annotations

from hamingja_dungeon.areas.vector import Vector
from hamingja_dungeon.direction.direction import Direction


class Action:
    def __init__(self, condition, effect):
        self.condition = condition
        self.effect = effect


def get_all_actions() -> dict[str, Action]:
    from hamingja_dungeon.areas.rooms.hallways.hallway_designer import HallwayDesigner

    def _valid_head(designer, head: Vector) -> bool:
        if not designer.area.in_childless_area(head):
            return False
        if head in designer.points:
            return False
        return True

    def _move(designer: HallwayDesigner, head: Vector, direction: Direction = None):
        designer.points.append(head)
        designer.head_point = head
        if direction is not None:
            designer.direction = direction
        designer.length += 1

    result = {}

    def forward_condition(designer: HallwayDesigner) -> bool:
        new_head = designer.head_point + designer.direction.unit_vector()
        return _valid_head(designer, new_head)

    def forward_effect(designer: HallwayDesigner) -> None:
        new_head = designer.head_point + designer.direction.unit_vector()
        _move(designer, new_head)

    result["move_forward"] = Action(condition=forward_condition, effect=forward_effect)

    def right_condition(designer: HallwayDesigner) -> bool:
        new_head = designer.head_point + designer.direction.right().unit_vector()
        return _valid_head(designer, new_head)

    def right_effect(designer: HallwayDesigner) -> None:
        new_direction = designer.direction.right()
        new_head = designer.head_point + new_direction.unit_vector()
        _move(designer, new_head, new_direction)

    result["turn_right"] = Action(condition=right_condition, effect=right_effect)

    def left_condition(designer: HallwayDesigner) -> bool:
        new_head = designer.head_point + designer.direction.right().unit_vector()
        return _valid_head(designer, new_head)

    def left_effect(designer: HallwayDesigner) -> None:
        new_direction = designer.direction.left()
        new_head = designer.head_point + new_direction.unit_vector()
        _move(designer, new_head, new_direction)

    result["turn_left"] = Action(condition=left_condition, effect=left_effect)

    return result
