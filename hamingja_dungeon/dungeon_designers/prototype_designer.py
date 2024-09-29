import random

from areas.dimension_range import DimensionSampler
from areas.dungeon_area import DungeonArea
from areas.exceptions import EmptyFitArea
from areas.rooms.room import Room, LRoom
from dungeon_designers.abstract_dungeon_area_designer import AbstractDungeonAreaDesigner
from dungeon_designers.config.dungeon_area_config import DungeonAreaConfig
from tile_types import carpet


class PrototypeDesigner(AbstractDungeonAreaDesigner):
    def __init__(self, config: DungeonAreaConfig):
        super().__init__(config)
        self._to_process: list[int] = []
        if config.room_size_method == "factor":
            self.room_dim_sampler = DimensionSampler.as_factor(
                config.size,
                config.factor_room_size,
            )
        elif config.room_size_method == "range":
            self.room_dim_sampler = DimensionSampler(config.range_room_size)
        else:
            self.room_dim_sampler = DimensionSampler.fixed(config.fixed_room_size)

    def _get_room(self):
        size = self.room_dim_sampler.sample()
        num = random.random()
        if num < 0.8:
            room = Room(size)
        else:
            room = LRoom(size)
        return room

    def _prepare(self, dungeon_area: DungeonArea):
        start_room = self._get_room()
        start_room.draw_inside(carpet)
        fit_area = dungeon_area.fit_in(start_room)
        if fit_area.is_empty():
            raise EmptyFitArea("Cannot fit the first room.")
        origin = fit_area.sample()
        id = dungeon_area.add_room(origin, start_room)
        self._to_process.append(id)

    def _add_room(self, dungeon_area: DungeonArea):
        if len(self._to_process) == 0:
            return -1
        tries = 0
        neighbour_id = random.choice(self._to_process)
        while tries < 20:
            room = self._get_room()
            try:
                new_room_id = dungeon_area.add_room_adjacent(room, neighbour_id)
                dungeon_area.make_entrance(neighbour_id, new_room_id)
            except EmptyFitArea:
                tries += 1
                continue
            self._to_process.append(new_room_id)
            return 1
        self._to_process.remove(neighbour_id)
        return 1

    def populate(self, dungeon_area: DungeonArea):
        self._prepare(dungeon_area)
        while dungeon_area.fullness() < 0.7:
            code = self._add_room(dungeon_area)
            if code == -1:
                return
