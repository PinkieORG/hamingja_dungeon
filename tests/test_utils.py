import numpy as np
from tcod import tcod

from areas.area import Area
from areas.dungeon_object import DungeonObject
from tile_types import floor
from utils.ascii_dungeon_generator.dungeon_renderer.renderer import Renderer

full_square = Area.from_array(
    np.array([[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]])
)

square = Area.from_array(
    np.array(
        [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 0, 0],
            [0, 0, 1, 1, 1, 1, 0, 0],
            [0, 0, 1, 1, 1, 1, 0, 0],
            [0, 0, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]
    )
)

l_shape = Area.from_array(
    np.array(
        [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
    )
)

c_shape = Area.from_array(
    np.array(
        [
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
    )
)

hole_shape = Area.from_array(
    np.array(
        [
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0],
            [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
    )
)


def get_test_areas() -> dict:
    return {
        "full square": full_square,
        "square": square,
        "L shape": l_shape,
        "C shape": c_shape,
        "hole shape": hole_shape,
    }


def get_test_dungeon_objects() -> dict[str, DungeonObject]:
    result = {}
    for name, area in get_test_areas().items():
        dungeon_object = DungeonObject(area.size, fill_value=floor)
        dungeon_object.mask = area.mask
        result[name] = dungeon_object
    return result


def print_name(name: str) -> None:
    print("======================")
    print(name)
    print("======================")


def print_test_areas(func, *args):
    areas = get_test_areas()
    for name, area in areas.items():
        print_name(name)
        print("original: ")
        area.print()
        print("result: ")
        func(area, *args).print()


def print_test_dungeon_objects(func, *args):
    dungeon_objects = get_test_dungeon_objects()
    for name, dungeon_object in dungeon_objects.items():
        print_name(name)
        print("original: ")
        print_dungeon_object(dungeon_object)
        print("result: ")
        func(dungeon_object, *args)
        print_dungeon_object(dungeon_object)


def print_dungeon_object(dungeon_object: DungeonObject) -> None:
    renderer = Renderer(dungeon_object)
    console = tcod.console.Console(height=dungeon_object.h, width=dungeon_object.w)
    renderer.render_console(console)
    output = " " + console.__str__()[1:-1]
    print(output)


# TODO testing class
