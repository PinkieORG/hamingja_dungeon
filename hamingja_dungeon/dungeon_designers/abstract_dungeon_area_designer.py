from abc import ABC, abstractmethod

from areas.dungeon_area import DungeonArea
from dungeon_designers.config.dungeon_area_config import DungeonAreaConfig


class AbstractDungeonAreaDesigner(ABC):
    def __init__(self, config: DungeonAreaConfig):
        self.config = config

    @abstractmethod
    def _get_room(self):
        raise NotImplemented

    @abstractmethod
    def populate(self, dungeon_area: DungeonArea):
        raise NotImplemented
