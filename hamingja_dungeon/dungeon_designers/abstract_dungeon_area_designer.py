from abc import ABC, abstractmethod

from hamingja_dungeon.dungeon_elements.sector import Sector
from hamingja_dungeon.dungeon_designers.config.dungeon_area_config import (
    DungeonAreaConfig,
)


class AbstractDungeonAreaDesigner(ABC):
    def __init__(self, config: DungeonAreaConfig):
        self.config = config

    @abstractmethod
    def _get_room(self):
        raise NotImplemented

    @abstractmethod
    def populate(self, dungeon_area: Sector):
        raise NotImplemented
