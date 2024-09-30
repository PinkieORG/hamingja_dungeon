from pydantic import BaseModel

from dungeon_designers.config.dungeon_area_config import DungeonAreaConfig


class ASCIIDungeonConfig(BaseModel):
    base_name: str = "dungeon"
    dungeon_area: DungeonAreaConfig
