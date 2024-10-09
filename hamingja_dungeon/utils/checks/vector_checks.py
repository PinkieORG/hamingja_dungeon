from hamingja_dungeon.utils.vector import Vector


def check_origin_is_positive(origin: Vector) -> None:
    if not origin.is_positive():
        raise ValueError("The origin has to be positive.")
