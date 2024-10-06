from __future__ import annotations
from hamingja_dungeon.utils.vector import Vector
from hamingja_dungeon.utils.direction import Direction


class HallwayAction:
    """An action that can be performed during drawing of the hallway.
    Has a condition that specify if the subsequent effect can be performed."""

    def __init__(self, condition, effect):
        self.condition = condition
        self.effect = effect


# TODO action to stop the drawing process not every hallway is maximum length if it isn't cornered.
# TODO crossections.
def get_all_actions() -> dict[str, HallwayAction]:
    from hamingja_dungeon.hallway_designers.hallway_designer import HallwayDesigner

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
        return designer.valid_head(new_head, designer.direction)

    def forward_effect(designer: HallwayDesigner) -> None:
        new_head = designer.head_point + designer.direction.unit_vector()
        _move(designer, new_head)

    result["move_forward"] = HallwayAction(
        condition=forward_condition, effect=forward_effect
    )

    def right_condition(designer: HallwayDesigner) -> bool:
        new_direction = designer.direction.right()
        new_head = designer.head_point + new_direction.unit_vector()
        return designer.valid_head(new_head, new_direction)

    def right_effect(designer: HallwayDesigner) -> None:
        new_direction = designer.direction.right()
        new_head = designer.head_point + new_direction.unit_vector()
        _move(designer, new_head, new_direction)

        action = designer.actions.get("turn_right")
        if action:
            action.decrease_likelihood(0.6)
        action = designer.actions.get("turn_left")
        if action:
            action.reset_likelihood()

    result["turn_right"] = HallwayAction(condition=right_condition, effect=right_effect)

    def left_condition(designer: HallwayDesigner) -> bool:
        new_direction = designer.direction.left()
        new_head = designer.head_point + new_direction.unit_vector()
        return designer.valid_head(new_head, new_direction)

    def left_effect(designer: HallwayDesigner) -> None:
        new_direction = designer.direction.left()
        new_head = designer.head_point + new_direction.unit_vector()
        _move(designer, new_head, new_direction)

        action = designer.actions.get("turn_left")
        if action:
            action.decrease_likelihood(0.6)
        action = designer.actions.get("turn_right")
        if action:
            action.reset_likelihood()

    result["turn_left"] = HallwayAction(condition=left_condition, effect=left_effect)

    return result
