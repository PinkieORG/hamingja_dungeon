import numpy as np
from tcod.console import Console

from areas.dungeon_object import DungeonObject
from tile_types import bg


class Renderer:

    def __init__(self, dungeon_object: DungeonObject):
        self.dungeon_object = dungeon_object

    def update(self):
        if isinstance(self.dungeon_object, DungeonObject):
            self.dungeon_object.draw_children()

    def render_console(self, console: Console):
        self.update()
        array = self.dungeon_object.mask
        tiles = self.dungeon_object.tiles
        console.rgb[0:console.height, 0:console.width] = np.where(array,
                                                                  tiles["dark"],
                                                                  bg["dark"])
