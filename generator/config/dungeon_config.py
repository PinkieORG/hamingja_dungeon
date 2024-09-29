from pydantic import BaseModel


class DungeonConfig(BaseModel):
    base_name: str = "dungeon"
    dungeon_area: DungeonAreaConfig
