from dungeon import DungeonArea
from dungeon.dungeon_designers.iterable_designers.room_neighbours_designer import (
    RoomNeighboursDesigner,
)
from tcod import tcod

from dungeon_gen.config.dungeon_config import DungeonConfig
from dungeon_gen.dungeon_generator.dungeon import Dungeon
from dungeon_gen.dungeon_renderer.renderer import Renderer


class DungeonGenerator:
    def __init__(self, dungeon_config: DungeonConfig):
        self.config = dungeon_config
        self.generated_count = 1

    def generate(self):
        dungeon_area = DungeonArea(self.config.dungeon_area.size)

        generator = RoomNeighboursDesigner(self.config.dungeon_area)
        generator.populate(dungeon_area)
        renderer = Renderer(dungeon_area)
        root_console = tcod.console.Console(
            height=self.config.dungeon_area.size[0],
            width=self.config.dungeon_area.size[1],
        )
        renderer.render_console(root_console)

        raw_output = root_console.__str__()
        raw_output = raw_output[1:-1]

        dungeon = Dungeon(
            raw_output, self.config.base_name + "_" + str(self.generated_count)
        )
        self.generated_count = self.generated_count + 1
        return dungeon
