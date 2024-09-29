from tcod import tcod

from areas.dungeon_area import DungeonArea
from config.dungeon_config import DungeonConfig
from dungeon_designers.prototype_designer import PrototypeDesigner
from dungeon_generator.dungeon import Dungeon
from dungeon_renderer.renderer import Renderer


class DungeonGenerator:
    def __init__(self, dungeon_config: DungeonConfig):
        self.config = dungeon_config
        self.generated_count = 1

    def generate(self):
        dungeon_area = DungeonArea(self.config.dungeon_area.size)

        generator = PrototypeDesigner(self.config.dungeon_area)
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
