from hamingja_dungeon.dungeon_elements.area import Area
from hamingja_dungeon.dungeon_elements.chamber import Chamber


def check_area_is_room(area: Area) -> None:
    if not isinstance(area, Chamber):
        raise ValueError("The area needs to be a room.")
